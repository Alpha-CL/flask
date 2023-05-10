from flask_sqlalchemy import SQLAlchemy


class DBMysqlSession:
    __db = None  # flask sqlalchemy
    __session = None
    __DBModel = None

    def __init__(self, db):
        db = db or SQLAlchemy()
        session = db.session

        self.__db = db
        self.__session = session
        self.__DBModel = db.Model

    def __enter__(self):
        return self.session

    def __exit__(self, *exc_infos):
        if exc_infos == (None, None, None):
            self.session.commit()
            self.session.close()
        else:
            self.session.rollback()

    @property
    def db(self):
        return self.__db

    @property
    def session(self):
        return self.__session

    @property
    def DBModel(self):
        return self.__DBModel

    def add(self, model):
        if issubclass(self.db, model):
            return self.db.session.add(model)

    def add_all(self, models):
        if type(models).__name__ in ['list', 'tuple']:
            return self.session.add_all(models)

    def delete(self, model, condition):
        res = self.db.session.query(model).filter(condition).first()
        if len(res) > 0:
            model = res[0]
            self.db.session.delete(model)

    def delete_all(self, model, condition):
        models = self.db.session.query(model).filter(condition).all()
        if len(models) > 0:
            self.db.session.delete(*models)

    def update(self, model, condition, callback=None):
        model = self.get(model, condition)
        if condition is not None:
            callback(model)
            return model

    def get(self, model, condition=None):
        db_data = self.db.session.query(model).filter(condition).all()
        if len(db_data) > 0:
            return db_data[0]

    def get_many(self, model, condition=None):
        if condition is not None:
            return self.db.session.query(model).filter(condition).many()
        else:
            return self.db.session.query(model).many()

    def get_all(self, model, condition=None):
        if condition is not None:
            return self.db.session.query(model).filter(condition).all()
        else:
            return self.db.session.query(model).all()

    def execute(self, sql):
        return self.db.session.execute(sql).cursor
