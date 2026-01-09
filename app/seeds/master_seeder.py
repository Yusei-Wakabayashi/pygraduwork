from flask_seeder import Seeder
from flask import current_app

class MasterSeeder(Seeder):
    def run(self):
        self.seed_elements()

        self.db = current_app.extensions["sqlalchemy"]
        self.Element = self.db.Model.registry._class_registry["Element"]
        # 作成したエレメントを取得
        self.element_map = {
            "fire":  self.Element.query.filter_by(element_name="fire").first(),
            "water": self.Element.query.filter_by(element_name="water").first(),
            "wind":  self.Element.query.filter_by(element_name="wind").first(),
        }

        self.seed_characters()
        self.seed_enemys()

    def seed_elements(self):
        db = current_app.extensions["sqlalchemy"]
        Element = db.Model.registry._class_registry["Element"]

        for name in ["fire", "water", "wind"]:
            db.session.add(Element(element_name=name))

        db.session.commit()

    def seed_characters(self):
        db = current_app.extensions["sqlalchemy"]

        Character = db.Model.registry._class_registry["Character"]
        CharacterElement = db.Model.registry._class_registry["CharacterElement"]

        characters = {
            "red": "red.png",
            "blue": "blue.png",
            "yellow": "yellow.png",
            "green": "green.png"
        }

        for name, image in characters.items():
            chara = Character(
                character_name=name,
                character_image_path="/static/image/" + image
            )

            elements = self.select_elements(name)
            for idx, element in enumerate(elements, start=1):
                chara.elements.append(
                    CharacterElement(element=element, slot=idx)
                )

            db.session.add(chara)

        db.session.commit()

    def seed_enemys(self):
        db = current_app.extensions["sqlalchemy"]

        Enemy = db.Model.registry._class_registry["Enemy"]
        EnemyElement = db.Model.registry._class_registry["EnemyElement"]

        enemys = {
            "red": "red.png",
            "blue": "blue.png",
            "yellow": "yellow.png",
            "green": "green.png"
        }

        for name, image in enemys.items():
            ene = Enemy(
                enemy_name=name,
                enemy_image_path="/static/image/" + image
            )

            elements = self.select_elements(name)
            for idx, element in enumerate(elements, start=1):
                ene.elements.append(
                    EnemyElement(element=element, slot=idx)
                )

            db.session.add(ene)

        db.session.commit()

    def select_elements(self, name):
        fire = self.element_map["fire"]
        water = self.element_map["water"]
        wind = self.element_map["wind"]

        mapping = {
            "red":    [fire, fire, fire, fire, fire, water, wind],
            "blue":   [fire, water, water, water, water, water, wind],
            "yellow": [fire, fire, fire, water, water, wind, wind],
            "green":  [fire, water, wind, wind, wind, wind, wind],
        }

        return mapping.get(
            name,
            [fire, fire, fire, water, water, wind, wind]
        )
