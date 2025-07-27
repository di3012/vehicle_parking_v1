from flask import Blueprint, request, jsonify
from models import db, ParkingLot, ParkingSpot, Reservation, User, Role
from datetime import datetime

admin_routes = Blueprint('admin_routes', __name__, url_prefix='/admin')

@admin_routes.route('/api/add_parkinglot', methods=['POST'])
def add_parking_lot():
    data = request.get_json()
    print("🟢 Received lot data:", data)

    try:
        lot = ParkingLot(
            city=data['city'],
            prime_location_name=data['prime_location_name'],
            price=data['price'],
            address=data['address'],
            pincode=data['pincode'],
            number_of_spots=data['number_of_spots']
        )
        db.session.add(lot)
        db.session.flush()  # get lot.id before commit

        # ✅ Create parking spots
        for _ in range(lot.number_of_spots):
            spot = ParkingSpot(lot_id=lot.id, status='A')
            db.session.add(spot)

        db.session.commit()

        return jsonify({'message': 'Parking lot and spots added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@admin_routes.route('/api/view_parkinglots', methods=['GET'])
def get_parking_lots():
    lots = ParkingLot.query.all()
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
            'created_at': lot.created_at.strftime('%Y-%m-%d')
        })
    return jsonify(result)

@admin_routes.route('/api/add_spots/<int:lot_id>', methods=['POST'])
def add_spots(lot_id):
    data = request.get_json()
    num_spots = data.get('count', 0)

    spots = [ParkingSpot(lot_id=lot_id, status='A') for _ in range(num_spots)]
    db.session.add_all(spots)
    db.session.commit()

    return jsonify({'message': f'{num_spots} spots added to lot {lot_id}'}), 201

@admin_routes.route('/api/reservations', methods=['GET'])
def view_reservations():
    reservations = Reservation.query.all()
    data = [{
        'id': r.id,
        'user_id': r.user_id,
        'spot_id': r.spot_id,
        'parking_time': r.parking_timestamp,
        'leaving_time': r.leaving_timestamp,
        'cost': r.parking_cost
    } for r in reservations]
    return jsonify(data), 200

@admin_routes.route('/api/delete_parkinglot/<int:lot_id>', methods=['DELETE'])
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    # Check if any spot is occupied
    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id).filter(ParkingSpot.status != 'A').count()
    if occupied_spots > 0:
        return jsonify({'error': 'Cannot delete parking lot. Some spots are still occupied.'}), 400

    try:
        # Optional: delete the spots first
        ParkingSpot.query.filter_by(lot_id=lot_id).delete()
        db.session.delete(lot)
        db.session.commit()
        return jsonify({'message': 'Parking lot deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_routes.route('/api/update_parkinglot/<int:lot_id>', methods=['PUT'])
def update_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()

    try:
        lot.city = data.get('city', lot.city)
        lot.prime_location_name = data.get('prime_location_name', lot.prime_location_name)
        lot.price = data.get('price', lot.price)
        lot.address = data.get('address', lot.address)
        lot.pincode = data.get('pincode', lot.pincode)
        lot.number_of_spots = data.get('number_of_spots', lot.number_of_spots)

        db.session.commit()
        return jsonify({'message': 'Parking lot updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@admin_routes.route('/api/get_parkinglot/<int:lot_id>', methods=['GET'])
def get_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    return jsonify({
        'id': lot.id,
        'city': lot.city,
        'prime_location_name': lot.prime_location_name,
        'price': lot.price,
        'address': lot.address,
        'pincode': lot.pincode,
        'number_of_spots': lot.number_of_spots
    })

@admin_routes.route('/api/lot_spots/<int:lot_id>', methods=['GET'])
def get_parking_spots_for_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    result = []

    for spot in lot.spots:
        spot_info = {
            'spot_id': spot.id,
            'status': spot.status
        }

        # Find the active reservation (leaving_timestamp is None)
        active_res = next((res for res in spot.reservation if res.leaving_timestamp is None), None)

        if active_res:
            spot_info['reserved_by'] = {
                'user_id': active_res.user.id,
                'name': active_res.user.name,
                'email': active_res.user.email,
                'vehicle_number': active_res.vehicle_number,
                'from': active_res.parking_timestamp,
            }

        result.append(spot_info)

    return jsonify(result), 200


@admin_routes.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = []

    for user in users:
        # Skip admin users
        if any(role.name == 'admin' for role in user.roles):
            continue

        result.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'reservation_count': len(user.reservations)
        })

    return jsonify(result)

@admin_routes.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if any(role.name == 'admin' for role in user.roles):
        return jsonify({'error': 'Cannot delete admin user'}), 400

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_routes.route('/api/admin_summary', methods=['GET'])
def get_admin_summary():
    lots = ParkingLot.query.all()
    users = User.query.filter(~User.roles.any(Role.name == 'admin')).all()
    total_reservations = Reservation.query.count()
    
    lot_data = []
    for lot in lots:
        spots = lot.spots
        total_spots = len(spots)
        occupied = sum(1 for s in spots if s.status == 'occupied')
        available = total_spots - occupied
        revenue = sum(r.parking_cost for s in spots for r in s.reservation if r.leaving_timestamp)

        lot_data.append({
            'lot_name': lot.prime_location_name,
            'total_spots': total_spots,
            'occupied': occupied,
            'available': available,
            'revenue': revenue
        })

    return jsonify({
        'total_users': len(users),
        'total_reservations': total_reservations,
        'lots': lot_data
    }), 200
