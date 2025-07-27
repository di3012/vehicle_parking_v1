from flask import Blueprint, request, jsonify, session
from models import db, ParkingLot, ParkingSpot, Reservation, User
from datetime import datetime, timedelta

user_routes = Blueprint('user_routes', __name__, url_prefix='/user')

@user_routes.route('/api/view_parkinglots')
def view_lots():
    lots = ParkingLot.query.all()
    return jsonify([
        {
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'price': lot.price,
            'address': lot.address,
            'pincode': lot.pincode,
            'number_of_spots': lot.number_of_spots
        } for lot in lots
    ])

@user_routes.route('/api/search_parkinglots', methods=['GET'])
def search_parking_lots():
    query = request.args.get('q', '').strip()
    print("🟢 Search API - session =", dict(session))
    if not query:
        # Return all if query is empty
        lots = ParkingLot.query.all()
    else:
        search = f"%{query.lower()}%"
        lots = ParkingLot.query.filter(
            db.or_(
                db.func.lower(ParkingLot.city).like(search),
                db.func.lower(ParkingLot.address).like(search),
                db.func.lower(ParkingLot.pincode).like(search),
                db.func.lower(ParkingLot.prime_location_name).like(search)
            )
        ).all()

    result = []
    for lot in lots:
        result.append({
            'id': lot.id,
            'city': lot.city,
            'prime_location_name': lot.prime_location_name,
            'price': lot.price,
            'address': lot.address,
            'pincode': lot.pincode,
            'number_of_spots': lot.number_of_spots,
            'created_at': lot.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(result)

@user_routes.route('/api/get_cities', methods=['GET'])
def get_cities():
    cities = db.session.query(ParkingLot.city).distinct().all()
    city_list = [city[0] for city in cities]
    return jsonify({'cities': city_list})


# @user_routes.route('/api/reserve_spot', methods=['POST'])
# def reserve_spot():
#     print("Current session:", dict(session))
#     user_id = session.get('user_id')  # Get user ID from session
#     if 'user_id' not in session:
#         return jsonify({'error': 'User not logged in'}), 401
    
#     # if 'user_id' not in session:
#     #     return jsonify({'error': 'User not logged in'}), 401

#     user_id = session['user_id']  # From session
#     data = request.get_json()

#     lot_id = data.get('lot_id')
#     date = data.get('date')
#     start_hour = int(data.get('start_hour'))
#     end_hour = int(data.get('end_hour'))

#     if end_hour <= start_hour:
#         return jsonify({'error': 'End hour must be after start hour'}), 400

#     try:
#         start_time = datetime.strptime(date, '%Y-%m-%d') + timedelta(hours=start_hour)
#         end_time = datetime.strptime(date, '%Y-%m-%d') + timedelta(hours=end_hour)
#     except:
#         return jsonify({'error': 'Invalid date or hour format'}), 400

#     lot = ParkingLot.query.get(lot_id)
#     if not lot:
#         return jsonify({'error': 'Parking lot not found'}), 404

#     available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
#     if not available_spot:
#         return jsonify({'error': 'No available spots'}), 400

#     duration_hours = (end_time - start_time).seconds // 3600
#     cost = duration_hours * lot.price

#     reservation = Reservation(
#         spot_id=available_spot.id,
#         user_id=user_id,
#         parking_timestamp=start_time,
#         leaving_timestamp=end_time,
#         parking_cost=cost
#     )
#     available_spot.status = 'O'

#     db.session.add(reservation)
#     db.session.commit()

#     return jsonify({'message': f'Reservation successful. Total cost: ₹{cost}'})

@user_routes.route('/api/reserve_now', methods=['POST'])
def reserve_now():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']
    data = request.get_json()
    lot_id = data.get('lot_id')

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({'error': 'Parking lot not found'}), 404

    # Check if user already has active reservation
    existing_res = Reservation.query.filter_by(user_id=user_id, leaving_timestamp=None).first()
    if existing_res:
        return jsonify({'error': 'You already have an active reservation'}), 400

    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not available_spot:
        return jsonify({'error': 'No available spots'}), 400

    reservation = Reservation(
        spot_id=available_spot.id,
        user_id=user_id,
        parking_timestamp=datetime.now(),
        leaving_timestamp=None,
        parking_cost=0,  # Will be calculated at vacate time
        vehicle_number=data.get('vehicle_number')
    )
    available_spot.status = 'O'

    db.session.add(reservation)
    db.session.commit()

    return jsonify({'message': 'Reservation successful', 'spot_id': available_spot.id})

@user_routes.route('/api/vacate_spot', methods=['POST'])
def vacate_spot():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']

    reservation = Reservation.query.filter_by(user_id=user_id, leaving_timestamp=None).first()
    if not reservation:
        return jsonify({'error': 'No active reservation found'}), 400

    reservation.leaving_timestamp = datetime.now()
    duration = (reservation.leaving_timestamp - reservation.parking_timestamp).seconds / 3600
    duration_hours = int(duration) if duration.is_integer() else int(duration) + 1

    lot = reservation.spot.lot
    reservation.parking_cost = duration_hours * lot.price

    # Update spot status to available
    reservation.spot.status = 'A'

    db.session.commit()

    return jsonify({
        'message': 'Spot vacated successfully',
        'duration_hours': duration_hours,
        'cost': reservation.parking_cost
    })


@user_routes.route('/api/current_reservations', methods=['GET'])
def current_reservations():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']

    # Fetch reservations where leaving time is in future (or still None)
    now = datetime.now()

    reservations = Reservation.query.filter_by(user_id=user_id).filter(
        (Reservation.leaving_timestamp == None) | (Reservation.leaving_timestamp > now)
    ).order_by(Reservation.parking_timestamp).all()

    result = []
    for res in reservations:
        spot = res.spot
        lot = spot.lot
        result.append({
            'reservation_id': res.id,
            'spot_id': spot.id,
            'lot_name': lot.prime_location_name,
            'address': lot.address,
            'city': lot.city,
            'vehicle_number': res.vehicle_number,
            'parking_timestamp': res.parking_timestamp.strftime('%Y-%m-%d %H:%M'),
            'leaving_timestamp': res.leaving_timestamp.strftime('%Y-%m-%d %H:%M') if res.leaving_timestamp else '—',
            'parking_cost': res.parking_cost
        })

    return jsonify(result), 200


@user_routes.route('/api/past_reservations', methods=['GET'])
def past_reservations():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']

    reservations = Reservation.query.filter_by(user_id=user_id).filter(
    Reservation.leaving_timestamp != None
).order_by(Reservation.leaving_timestamp.desc()).all()

    result = []
    for res in reservations:
        spot = res.spot
        lot = spot.lot
        result.append({
            'reservation_id': res.id,
            'spot_id': spot.id,
            'lot_name': lot.prime_location_name,
            'address': lot.address,
            'city': lot.city,
            'vehicle_number': res.vehicle_number,
            'parking_timestamp': res.parking_timestamp.strftime('%Y-%m-%d %H:%M'),
            'leaving_timestamp': res.leaving_timestamp.strftime('%Y-%m-%d %H:%M'),
            'parking_cost': res.parking_cost
        })

    return jsonify(result), 200

@user_routes.route('api/user_summary/<int:user_id>', methods=['GET'])
def user_summary(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    reservations = Reservation.query.filter_by(user_id=user_id).all()

    total_reservations = len(reservations)
    total_parking_hours = 0
    total_cost = 0
    lot_count = {}

    for res in reservations:
        if res.leaving_timestamp:
            hours = (res.leaving_timestamp - res.parking_timestamp).total_seconds() / 3600
            total_parking_hours += hours
        total_cost += res.parking_cost

        lot = res.spot.lot
        if lot:
            lot_count[lot.prime_location_name] = lot_count.get(lot.prime_location_name, 0) + 1

    most_used_lot = max(lot_count, key=lot_count.get) if lot_count else "N/A"

    return jsonify({
        "total_reservations": total_reservations,
        "total_parking_hours": round(total_parking_hours, 2),
        "total_cost": round(total_cost, 2),
        "most_used_lot": most_used_lot
    })


