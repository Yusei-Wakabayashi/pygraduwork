from flask import Flask, Blueprint, render_template, request, redirect, send_file, jsonify, session
from flask_app import db
from flask_app.models import Character, Game, Enemy, Element, CharacterElement, Game, EnemyElement
import datetime
import random

app = Flask(__name__)
app.secret_key = "secret0303"

index_bp = Blueprint('index', __name__, url_prefix='/')

@index_bp.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_file("static/image/favicon.ico", mimetype="image/icon")

@index_bp.route("/", methods=["GET", "POST"])
def index():
    # your code
    hoge_lists = db.session.query(Character).all()
    return render_template("index.html")

# タイトル画面
@index_bp.route('/title', methods=["GET"])
def title():
    if "user_id" not in session:
        session["user_id"] = (
            "test"
            + datetime.datetime.now().isoformat()
            + str(random.randint(0, 1000))
        )
    return render_template("title.html")

# キャラクター選択画面
@index_bp.route('/select/character', methods=["GET"])
def selectcharacter():

    return render_template("selectcharacter.html")

# キャラクター詳細画面
@index_bp.route('/detail/character', methods=["GET"])
def detailcharacter():

    key = request.args.get("key", "")
    return key

# キャラクター追加画面
@index_bp.route('/add/character', methods=["GET"])
def addcharacter():
    return render_template("addcharacter.html")

# キャラクター完成画面
@index_bp.route('/finish/character', methods=["GET"])
def finishcharacter():
    pass

# ゲーム画面
@index_bp.route('/game', methods=["GET"])
def game():
    return render_template("game.html")

# キャラクター追加
@index_bp.route('/character/add', methods=["GET"])
def characteradd():
    # 本文から情報を取得しAIで性格分析
    fire  = Element.query.filter_by(element_name="fire").first()
    water = Element.query.filter_by(element_name="water").first()
    wind  = Element.query.filter_by(element_name="wind").first()

    character = Character(
        character_name="red",
        character_image_path="/static/img/red.png"
    )

    character.elements = [
        CharacterElement(element=fire,  slot=1),
        CharacterElement(element=water, slot=2),
        CharacterElement(element=wind,  slot=3),
    ]

    db.session.add(character)
    db.session.commit()
    return "text"

# キャラクター取得
@index_bp.route('/character/list', methods=["GET"])
def characterlist():
    character = Character.query.all()
    return jsonify([c.to_dict() for c in character])

# ゲーム情報取得
@index_bp.route('/game/info', methods=["GET"])
def gameinfo():
    # -----------------------------
    # セッションチェック
    # -----------------------------
    # ゲームIDがセッションに存在しない場合はエラーコード返却
    if not session.get("game_id"):
        return "3"

    # -----------------------------
    # ゲーム情報取得
    # -----------------------------
    # 現在進行中のゲームを取得
    game = Game.query.filter_by(
        game_id=session.get("game_id")
    ).first()

    # dict形式に変換（API返却用）
    game = game.to_dict()

    # -----------------------------
    # 敵・キャラクターの属性スロット取得
    # -----------------------------
    enemyElements = EnemyElement.query.filter_by(
        enemy_id=game["enemy_id"]
    ).all()

    characterElements = CharacterElement.query.filter_by(
        character_id=game["character_id"]
    ).all()

    # -----------------------------
    # 属性表示用データ初期化
    # -----------------------------
    # enemy: 未公開のため "hidden"
    # character: 実際の属性名を表示
    enemy_elements = {}
    character_elements = {}

    # -----------------------------
    # 敵の属性スロット構築
    # -----------------------------
    for enemyElement in enemyElements:
        # slot番号をキーにし、値は非公開扱い
        enemy_elements[enemyElement.slot] = "hidden"

    # -----------------------------
    # キャラクターの属性スロット構築
    # -----------------------------
    for characterElement in characterElements:
        # 紐づく属性情報取得
        character_element = Element.query.filter_by(
            element_id=characterElement.element_id
        ).first()

        # slot番号をキーに属性名をセット
        character_elements[characterElement.slot] = character_element.element_name

    # -----------------------------
    # 敵の使用済み属性を除外
    # -----------------------------
    if game["enemy_used"]:
        enemy_useds = list(game["enemy_used"])
        for enemyuse in enemy_useds:
            enemy_elements.pop(int(enemyuse), None)

    # -----------------------------
    # キャラクターの使用済み属性を除外
    # -----------------------------
    if game["character_used"]:
        character_useds = list(game["character_used"])
        for characteruse in character_useds:
            character_elements.pop(int(characteruse), None)

    # -----------------------------
    # レスポンス用データ追加
    # -----------------------------
    game["enemy_element"] = enemy_elements
    game["character_element"] = character_elements

    # -----------------------------
    # JSONで返却
    # -----------------------------
    return jsonify(game)

@index_bp.route('/game/update', methods=["POST"])
def gameupdate():
    # -----------------------------
    # リクエスト取得
    # -----------------------------
    post_data = request.get_json()
    character_select = int(post_data["slot"])

    # -----------------------------
    # ゲーム情報取得
    # -----------------------------
    game = Game.query.get(session.get("game_id"))
    if not game:
        abort(404)

    # -----------------------------
    # 敵の属性スロット一覧取得
    # -----------------------------
    enemy_elements = EnemyElement.query.filter_by(
        enemy_id=game.enemy_id
    ).all()

    # EnemyElement に存在する全 slot（正の集合）
    all_enemy_slots = {e.slot for e in enemy_elements}

    # -----------------------------
    # 使用済みスロット取得
    # -----------------------------
    enemy_used_slots = set(map(int, game.enemy_used)) if game.enemy_used else set()
    character_used_slots = set(map(int, game.character_used)) if game.character_used else set()

    # -----------------------------
    # スロット重複チェック（プレイヤー）
    # -----------------------------
    if character_select in character_used_slots:
        return jsonify({
            "error": "このスロットはすでに使用されています"
        }), 400

    # -----------------------------
    # 敵の未使用スロット算出
    # -----------------------------
    available_enemy_slots = all_enemy_slots - enemy_used_slots

    if not available_enemy_slots:
        return jsonify({"error": "敵が使用可能なスロットがありません"}), 400

    # -----------------------------
    # 敵のターン（slot決定）
    # -----------------------------
    enemy_select = enemy_turn(list(available_enemy_slots))

    # -----------------------------
    # EnemyElement取得（slotは一意なので必ず1件）
    # -----------------------------
    enemy_ce = EnemyElement.query.filter_by(
        enemy_id=game.enemy_id,
        slot=enemy_select
    ).first()
    if enemy_ce is None:
        return jsonify({"error": "invalid enemy slot"}), 400

    enemy_element = enemy_ce.element

    # -----------------------------
    # プレイヤーの属性取得
    # -----------------------------
    ce = CharacterElement.query.filter_by(
        character_id=game.character_id,
        slot=character_select
    ).first()

    if not ce:
        return jsonify({
            "error": "無効なプレイヤースロットです"
        }), 400

    character_element = ce.element

    # -----------------------------
    # 勝敗判定
    # -----------------------------
    result = judge_battle(enemy_element, character_element)

    # -----------------------------
    # 勝敗結果を count に反映
    # -----------------------------
    counts = list(game.count)

    for i, c in enumerate(counts):
        if c == "1":
            counts[i] = {2: "2", 1: "3", 0: "4"}[result]
            break

    game.count = ''.join(counts)

    # -----------------------------
    # 使用済みスロット記録（重複なし保証）
    # -----------------------------
    enemy_used_slots.add(enemy_select)
    character_used_slots.add(character_select)
    game.enemy_used = ''.join(map(str, sorted(enemy_used_slots)))
    game.character_used = ''.join(map(str, sorted(character_used_slots)))


    # -----------------------------
    # DB反映
    # -----------------------------
    db.session.commit()

    # -----------------------------
    # フロントへ返却
    # -----------------------------
    return jsonify({
        "count": counts,
        "enemy_slot": enemy_select,
        "result": result
    })


# ゲーム開始(ゲームオブジェクト作成)
@index_bp.route('/game/init', methods=["POST"])
def gameinit():
    # if session.get("game_id"):
    #     return "3"
    post_data = request.get_json()
    character = Character.query.filter_by(character_id=post_data['character_id']).first()
    enemy = Enemy.query.filter_by(enemy_id=1).first()
    game = Game(
        session = session['user_id'],
        count = "1111111",
        result = 1,
        enemy = enemy,
        enemy_used = "",
        character = character,
        character_used = ""
    )
    db.session.add(game)
    db.session.flush()
    game_id = game.game_id
    db.session.commit()
    # sessionにゲームid保存
    session['game_id'] = (game_id)
    return jsonify(game_id)


def enemy_turn(available_slots):
    return random.choice(available_slots)

def judge_battle(enemy, character):
    map = {"fire":0, "wind":1, "water":2}
    result = (map[character.element_name] - map[enemy.element_name]) % 3
    return result
