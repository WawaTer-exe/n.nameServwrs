import sqlite3
import json
from flask import Flask, request, jsonify, render_template_string, redirect, url_for

app = Flask(__name__)
PORT = 8080
DB_FILE = "reborn_rec.db"

# ==============================================================================
# DATABASE & ARCHIVE UTILITIES
# ==============================================================================
def init_db():
    """Initializes local tables and seeds a clean baseline profile."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        # User Profiles Storage Array
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                level INTEGER DEFAULT 30,
                xp INTEGER DEFAULT 15000,
                tokens INTEGER DEFAULT 5000,
                avatar_data TEXT NOT NULL,
                is_active INTEGER DEFAULT 0
            )
        ''')
        
        # Cosmetic Items Matrix Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                item_key TEXT NOT NULL,
                is_equipped INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Auto-seed the database if it's currently unpopulated
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            # Baseline default configuration representing standard legacy state values
            default_avatar = json.dumps({"SkinColor": 1, "FaceType": 0, "HairType": 2, "HairColor": 3})
            cursor.execute('''
                INSERT INTO users (username, display_name, avatar_data, is_active)
                VALUES ('RebornPlayer', 'Dorm Guest', ?, 1)
            ''', (default_avatar,))
            
            user_id = cursor.lastrowid
            default_items = ["hair_default", "shirt_reborn_developer", "gloves_laser_tag", "avatar_hat_bucket"]
            for item in default_items:
                cursor.execute("INSERT INTO inventory (user_id, item_key, is_equipped) VALUES (?, ?, 0)", (user_id, item))
        conn.commit()

def get_active_user():
    """Retrieves the active profile configuration mapping array."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE is_active = 1 LIMIT 1")
        user = cursor.fetchone()
        if user:
            return dict(user)
        # Safe fallback routine if profile active state flags get desynced
        cursor.execute("SELECT * FROM users LIMIT 1")
        return dict(cursor.fetchone())

def get_user_inventory(user_id):
    """Fetches custom wardrobe inventory records for the target profile."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE user_id = ?", (user_id,))
        return [dict(row) for row in cursor.fetchall()]

# ==============================================================================
# WEB CONTROL CENTER HTML (LAUNCHER DASHBOARD STYLE)
# ==============================================================================
HTML_PANEL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RebornRec v2 - Server Hub</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #0f0f12; color: #f1f1f4; margin: 0; padding: 40px; }
        .container { max-width: 900px; margin: 0 auto; }
        header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #252530; padding-bottom: 20px; margin-bottom: 30px; }
        h1 { color: #ff4747; margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 1px; }
        .badge { background: #1b4d22; padding: 6px 12px; border-radius: 20px; font-size: 12px; color: #a2ffa2; font-weight: bold; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: #171721; border: 1px solid #252530; border-radius: 12px; padding: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        h2 { margin-top: 0; font-size: 18px; color: #fff; border-left: 4px solid #ff4747; padding-left: 10px; }
        .form-group { margin-bottom: 18px; }
        label { display: block; margin-bottom: 6px; font-size: 13px; color: #a0a0b0; font-weight: 600; }
        input[type="text"], input[type="number"] { width: 100%; padding: 12px; background: #1f1f2e; border: 1px solid #2d2d3f; color: #fff; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
        input:focus { border-color: #ff4747; outline: none; }
        .btn { background: #ff4747; color: white; border: none; padding: 12px 24px; font-size: 14px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; transition: background 0.2s; }
        .btn:hover { background: #e03636; }
        ul { list-style: none; padding: 0; margin: 0; max-height: 180px; overflow-y: auto; }
        li { background: #1f1f2e; padding: 10px 14px; margin-bottom: 8px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; font-size: 14px; }
        .delete-link { color: #ff4747; text-decoration: none; font-size: 12px; font-weight: bold; }
        .delete-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>RebornRec Control Center</h1>
                <div style="color: #606070; margin-top: 4px;">Localhost Emulation Layer & Account Sandbox Engine</div>
            </div>
            <div class="badge">SERVER STATUS: ACTIVE (PORT 8080)</div>
        </header>

        <div class="grid">
            <!-- Account and Stats Panel -->
            <div class="card">
                <h2>Profile Editor</h2>
                <form method="POST" action="/panel/save-profile">
                    <div class="form-group">
                        <label>Avatar Display Name</label>
                        <input type="text" name="display_name" value="{{ user.display_name }}">
                    </div>
                    <div class="form-group">
                        <label>Player Level Range (1-30)</label>
                        <input type="number" name="level" value="{{ user.level }}" min="1" max="30">
                    </div>
                    <div class="form-group">
                        <label>Token Bank Balance</label>
                        <input type="number" name="tokens" value="{{ user.tokens }}">
                    </div>
                    <button type="submit" class="btn">Apply Changes</button>
                </form>
            </div>

            <!-- Custom Unlocked Items Drawer -->
            <div class="card">
                <h2>Wardrobe Locker</h2>
                <form method="POST" action="/panel/add-item" style="margin-bottom: 20px; display: flex; gap: 10px;">
                    <input type="text" name="item_key" placeholder="e.g., shirt_reborn_developer" required style="flex: 1;">
                    <button type="submit" class="btn" style="width: auto;">Unlock</button>
                </form>
                
                <label style="margin-bottom: 10px;">Currently Unlocked Items</label>
                <ul>
                    {% for item in items %}
                    <li>
                        <span>📦 {{ item.item_key }}</span>
                        <a href="/panel/delete-item/{{ item.id }}" class="delete-link">Remove</a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index_panel():
    user = get_active_user()
    items = get_user_inventory(user['id'])
    return render_template_string(HTML_PANEL, user=user, items=items)

@app.route('/panel/save-profile', methods=['POST'])
def save_profile():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET display_name = ?, level = ?, tokens = ? WHERE is_active = 1", 
                       (request.form.get('display_name'), request.form.get('level'), request.form.get('tokens')))
        conn.commit()
    return redirect(url_for('index_panel'))

@app.route('/panel/add-item', methods=['POST'])
def add_inventory_item():
    item_key = request.form.get('item_key').strip()
    if item_key:
        user = get_active_user()
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO inventory (user_id, item_key) VALUES (?, ?)", (user['id'], item_key))
            conn.commit()
    return redirect(url_for('index_panel'))

@app.route('/panel/delete-item/<int:item_id>', methods=['GET'])
def delete_inventory_item(item_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        conn.commit()
    return redirect(url_for('index_panel'))


# ==============================================================================
# HIGH-FIDELITY LEGACY CLIENT REST API PIPELINE
# ==============================================================================

@app.route('/api/config/v2', methods=['GET'])
def client_config_v2():
    return jsonify({"IsMaintenanceMode": False, "StripePublishableKey": "pk_reborn", "RegistrationStatus": 0})

@app.route('/api/auth/v4/loginPlatform', methods=['POST'])
def client_login_platform():
    user = get_active_user()
    return jsonify({"Token": "reborn_session_key", "PlayerId": user['id'], "IsNewAccount": False, "Result": 0})

@app.route('/connect/token', methods=['POST'])
    return jsonify({"access_token": "reborn_session_key", "expires_in": 86400, "token_type": "Bearer"})

@app.route('/api/players/v1/me', methods=['GET'])
def client_get_me():
    user = get_active_user()
    return jsonify({
        "PlayerId": user['id'], 
        "Username": user['username'], 
        "DisplayName": user['display_name'],
        "RegistrationStatus": 2, 
        "IsJunior": False, 
        "Platforms": 1
    })

@app.route('/api/players/v1', methods=['GET'])
def client_get_players():
    user = get_active_user()
    return jsonify([{
        "PlayerId": user['id'], 
        "Username": user['username'], 
        "DisplayName": user['display_name'],
        "RegistrationStatus": 2, 
        "IsJunior": False
    }])

@app.route('/api/avatar/v2/saved', methods=['GET'])
def client_get_avatar_saved():
    user = get_active_user()
    return jsonify([{"OutfitId": "reborn_outfit", "AvatarData": user['avatar_data']}])

@app.route('/api/avatar/v2/saved', methods=['POST'])
def client_save_avatar():
    payload = request.get_json()
    if payload and 'AvatarData' in payload:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET avatar_data = ? WHERE is_active = 1", (json.dumps(payload['AvatarData']),))
            conn.commit()
    return jsonify({"Result": True})

@app.route('/api/avatar/v3/current', methods=['GET'])
def client_get_avatar_current():
    user = get_active_user()
    try:
        data = json.loads(user['avatar_data'])
    except:
        data = {"SkinColor": 0, "FaceType": 0, "HairType": 0, "HairColor": 0}
    return jsonify({
        "PlayerId": user['id'], 
        "SkinColor": data.get("SkinColor", 0), 
        "FaceType": data.get("FaceType", 0),
        "HairType": data.get("HairType", 0), 
        "HairColor": data.get("HairColor", 0), 
        "OutfitData": "{}"
    })

@app.route('/api/currency/v1/wallet', methods=['GET'])
def client_get_wallet():
    user = get_active_user()
    return jsonify([{"CurrencyType": 1, "Balance": int(user['tokens'])}])

@app.route('/api/inventory/v1/me', methods=['GET'])
def client_get_inventory():
    user = get_active_user()
    db_items = get_user_inventory(user['id'])
    # Converts database items to exact JSON matrix schema the old client watch expect
    client_inventory = []
    for index, item in enumerate(db_items):
        client_inventory.append({
            "PlayerItemDetailId": index + 100,
            "ItemKey": item['item_key'],
            "Type": 1,
            "Count": 1
        })
    return jsonify(client_inventory)

@app.route('/api/players/v1/progression', methods=['GET'])
def client_get_progression():
    user = get_active_user()
    return jsonify({"PlayerId": user['id'], "Level": int(user['level']), "XP": int(user['xp'])})

@app.route('/api/rooms/v4/home', methods=['GET'])
def client_get_home():
    user = get_active_user()
    return jsonify({"RoomId": 1, "Name": "DormRoom", "Data": "{}", "CreatorPlayerId": user['id']})

@app.route('/api/rooms/v2/search', methods=['GET'])
def client_room_search():
    query = request.args.get('search', '').lower()
    return jsonify([{
        "RoomId": 99, 
        "Name": query if query else "Paintball", 
        "Description": "Offline Emulated Sandbox Arena",
        "CreatorPlayerId": 1, 
        "MaxPlayers": 10, 
        "IsFeatured": True, 
        "CustomGameSceneKeys": []
    }])

@app.route('/api/matchmaking/v1/photonconfig', methods=['GET'])
def client_photon_config():
    """Forces the client into a single player sandbox engine loopback address."""
    return jsonify({
        "AppId": "00000000-0000-0000-0000-000000000000",
        "AppVersion": "2018_Build_Era",
        "Region": "US",
        "MasterServerAddress": "127.0.0.1"
    })

# Necessary baseline stub handlers for empty data frames
@app.route('/api/relationships/v1/get', methods=['GET'])
def client_relationships(): 
    return jsonify([])

@app.route('/api/rooms/v2/myrooms', methods=['GET'])
def client_myrooms(): 
    return jsonify([])

# ==============================================================================
# ENGINE MAIN EXECUTION RUNTIME ENTRYPOINT
# ==============================================================================
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=PORT, debug=True)
