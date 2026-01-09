from flask_app import db

# elementtable
class Element(db.Model):
    __tablename__ = "elements"
    element_id = db.Column(db.Integer, primary_key = True)
    element_name = db.Column(db.String(255), nullable = False)
    # 宛先指定
    characters = db.relationship(
        "CharacterElement",
        back_populates="element"
    )
    # 宛先指定
    enemys = db.relationship(
        "EnemyElement",
        back_populates="element"
    )
    def to_dict(self):
        return {
            "id": self.element_id,
            "name": self.element_name
        }

#Charactertable
class Character(db.Model):
    __tablename__ = "characters"

    character_id = db.Column(db.Integer, primary_key=True)
    character_image_path = db.Column(db.String(255), nullable=False)
    character_name = db.Column(db.String(255), nullable=False)

    games = db.relationship("Game", back_populates="character")

    elements = db.relationship(
        "CharacterElement",
        back_populates="character",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.character_id,
            "name": self.character_name,
            "image": self.character_image_path,
            "elements": [
                {
                    "slot": ce.slot,
                    "id": ce.element.element_id,
                    "name": ce.element.element_name
                }
                for ce in sorted(self.elements, key=lambda x: x.slot)
            ]
        }
    
# enemytable
class Enemy(db.Model):
    __tablename__ = "enemys"

    enemy_id = db.Column(db.Integer, primary_key=True)
    enemy_image_path = db.Column(db.String(255), nullable=False)
    enemy_name = db.Column(db.String(255), nullable=False)

    games = db.relationship("Game", back_populates="enemy")

    elements = db.relationship(
        "EnemyElement",
        back_populates="enemy",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.enemy_id,
            "image": self.enemy_image_path,
            "name": self.enemy_name,
            "elements": [
                {
                    "slot": ce.slot,
                    "id": ce.element.element_id,
                    "name": ce.element.element_name
                }
                for ce in sorted(self.elements, key=lambda x: x.slot)
            ]
        }
    
class CharacterElement(db.Model):
    __tablename__ = "character_elements"

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(
        db.Integer,
        db.ForeignKey("characters.character_id"),
        nullable=False
    )
    element_id = db.Column(
        db.Integer,
        db.ForeignKey("elements.element_id"),
        nullable=False
    )
    slot = db.Column(db.Integer, nullable=False)

    character = db.relationship("Character", back_populates="elements")
    element = db.relationship("Element", back_populates="characters")

class EnemyElement(db.Model):
    __tablename__ = "enemy_elements"

    id = db.Column(db.Integer, primary_key=True)
    enemy_id = db.Column(
        db.Integer,
        db.ForeignKey("enemys.enemy_id"),
        nullable=False
    )
    element_id = db.Column(
        db.Integer,
        db.ForeignKey("elements.element_id"),
        nullable=False
    )
    slot = db.Column(db.Integer, nullable=False)

    enemy = db.relationship("Enemy", back_populates="elements")
    element = db.relationship("Element", back_populates="enemys")

# gametable
class Game(db.Model):
    __tablename__ = "games"

    game_id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(255), nullable=False)
    count = db.Column(db.String(255), nullable=False)
    result = db.Column(db.Integer, nullable=False)

    enemy_id = db.Column(
        db.Integer,
        db.ForeignKey('enemys.enemy_id'),
        nullable=False
    )
    character_id = db.Column(
        db.Integer,
        db.ForeignKey('characters.character_id'),
        nullable=False
    )

    enemy_used = db.Column(db.String(255))
    character_used = db.Column(db.String(255))

    enemy = db.relationship("Enemy", back_populates="games")
    character = db.relationship("Character", back_populates="games")
    def to_dict(self):
        return {
            "id": self.game_id,
            "character_id": self.character_id,
            "character_used": self.character_used,
            "enemy_id": self.enemy_id,
            "enemy_used": self.enemy_used,
            "count": self.count,
            "result": self.result
        }
