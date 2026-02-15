"""Tests for BaseModel and model utilities."""
from datetime import datetime
from app import db
from models import BaseModel


# Concrete model for testing the abstract BaseModel
class SampleModel(BaseModel):
    __tablename__ = 'sample_models'
    name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        data = super().to_dict()
        data.update({'name': self.name})
        return data


class TestBaseModelFields:
    def test_create_record(self, app):
        with app.app_context():
            db.create_all()
            record = SampleModel(name='test')
            db.session.add(record)
            db.session.commit()
            assert record.id is not None

    def test_created_at_auto_set(self, app):
        with app.app_context():
            db.create_all()
            record = SampleModel(name='test')
            db.session.add(record)
            db.session.commit()
            assert record.created_at is not None
            assert isinstance(record.created_at, datetime)

    def test_updated_at_auto_set(self, app):
        with app.app_context():
            db.create_all()
            record = SampleModel(name='test')
            db.session.add(record)
            db.session.commit()
            assert record.updated_at is not None
            assert isinstance(record.updated_at, datetime)


class TestBaseModelToDict:
    def test_to_dict_contains_id(self, app):
        with app.app_context():
            db.create_all()
            record = SampleModel(name='test')
            db.session.add(record)
            db.session.commit()
            data = record.to_dict()
            assert 'id' in data
            assert data['id'] == record.id

    def test_to_dict_contains_timestamps(self, app):
        with app.app_context():
            db.create_all()
            record = SampleModel(name='test')
            db.session.add(record)
            db.session.commit()
            data = record.to_dict()
            assert 'created_at' in data
            assert 'updated_at' in data

    def test_to_dict_timestamps_are_iso_format(self, app):
        with app.app_context():
            db.create_all()
            record = SampleModel(name='test')
            db.session.add(record)
            db.session.commit()
            data = record.to_dict()
            # Verify ISO format by parsing back
            datetime.fromisoformat(data['created_at'])
            datetime.fromisoformat(data['updated_at'])

    def test_child_to_dict_extends_base(self, app):
        with app.app_context():
            db.create_all()
            record = SampleModel(name='test')
            db.session.add(record)
            db.session.commit()
            data = record.to_dict()
            assert 'name' in data
            assert data['name'] == 'test'

    def test_abstract_model_not_a_table(self):
        assert BaseModel.__abstract__ is True
