from flask import Flask, request, jsonify
import sqlite3
from generate_track import generate

app = Flask('delivery')

#Создание доставки
@app.route('/create_delivery_request', methods=['POST'])
def create_delivery():
    params = request.json
    
    sender_name = params.get('sender_name')
    sender_address = params.get('sender_address')
    getter_name = params.get('getter_name')
    getter_address = params.get('getter_address')
    info = params.get('info')
    status = "created"
    id = 0
    track = generate()
    
    try:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        
        c.execute('''
        SELECT * FROM deliveries ORDER BY id DESC LIMIT 1
        ''')
        last = c.fetchone()
        if(last):
            id = last[0] + 1
        else:
            id = 1
        
        c.execute('''
INSERT INTO deliveries(id, sender_name, sender_address, getter_name, getter_address, info, status, track)
VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                ''', (id, sender_name, sender_address, getter_name, getter_address, info, status, track))
                
        db.commit()
        return jsonify({"status": "success", "message": f"delivery created, track: {track}, id: {id}"}), 201
    except Exception as e:
        print(f'falied to create delivery: {e}')
        return jsonify({"status": "failed", "message": "failed to create delivery"}), 500
    finally:
        db.close()
        
#Получение информации о доставке
@app.route('/get_delivery_info', methods=['GET'])
def get_delivery_info():
        id = request.args.get('id')
        try:
            db = sqlite3.connect("database.db")
            c = db.cursor()
            c.execute('''SELECT * FROM deliveries WHERE id = ?''', (id,))
            delivery_info = c.fetchone()
            
            if delivery_info is None:
                return jsonify({"status": "failed", "message": "not found"}), 404
            
            data = {
                "sender_name": delivery_info[1],
                "sender_address": delivery_info[2],
                "getter_name": delivery_info[3],
                "getter_address": delivery_info[4],
                "info": delivery_info[5],
                "status": delivery_info[6],
                "track": delivery_info[7]
            }
            return jsonify({"status": "success", "message": data}), 200
            
        except Exception as e:
            print(colored(f'failed to get info: {e}'), 'red')
            return jsonify({"status": "failed", "message": "failed to get info"}), 500
        finally:
            db.close()
            
@app.route('/change_delivery_status', methods=['POST'])
def change_status():
            db = sqlite3.connect('database.db')
            c = db.cursor()
            try:
                params = request.json
                
                id = params.get('id')
                new_status = params.get('status')
                
                c.execute('''
                SELECT * FROM deliveries WHERE id = ?
                ''', (id,))
                deliver = c.fetchone()
                if deliver is None:
                    print('failed: not found')
                    return jsonify({"status": "failed", "message": "not found"}), 404
                if(deliver[6] == 'end'):
                    print('cannot change status: deliver delivered')
                    return jsonify({"status": "failed", "message": "Forbidden"}), 403
                    
                c.execute('''UPDATE deliveries SET status = ? WHERE id = ?''', (new_status, id))
                 
                db.commit()
                return jsonify({"status": "success", "message": "status changed"}), 200
            except Exception as e:
                print(f"failed: {e}")
                return jsonify({"status": "failed", "message": "failed to change status"}), 500
            finally:
                db.close()
            
@app.route('/delete_delivery', methods=['DELETE'])
def delete_delivery():
        db = sqlite3.connect('database.db')
        c = db.cursor()
        try:
            id = int(request.args.get('id'))
            print(type(id))
            
            c.execute('''
            SELECT * FROM deliveries WHERE id = ?
            ''', (id,))
            delivery = c.fetchone()
            if delivery is None:
                print('Not found')
                return jsonify({"status": "failed", "message": "not found"}), 404
            if delivery[6] != 'created':
                print("Canot be delete this delivery")
                return jsonify({"status": "failed", "message": "Forbidden"}), 403
            
            c.execute('''
            DELETE FROM deliveries WHERE id = ?
            ''', (id,))
            print('ok')
            c.execute('''SELECT * FROM deliveries WHERE id > ?''', (id,))
            all = c.fetchall()
            print('ok')
            for i in all:
                new_id = i[0] - 1
                c.execute('''
                UPDATE deliveries SET id = ? WHERE id = ?
                ''', (new_id, i[0]))
            db.commit()
            
            print('Delivery deleted')
            return jsonify({"status": "success", "message": "delivery deleted"}), 200
        except Exception as e:
            print(f"failed to delete delivery: {e}")
            return jsonify({"status": "failed", "message": "failed to delete delivery"}), 500
        finally:
            db.close()
        
if __name__ == "__main__":
    app.run(debug=True)