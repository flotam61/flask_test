from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Text, DateTime, Integer, func, create_engine

app = Flask('app')
PG_GSN = 'postgresql://flores:zxczxc@localhost:5432/avito'

engine = create_engine(PG_GSN)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Ad(Base):
    __tablename__ = 'avito'
    id = Column(Integer, primary_key=True)
    article = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime, server_default=func.now())
    owner = Column(String(20), nullable=False)


def get_ad(session: Session, user_id: int):
    ad = session.query(Ad).get(user_id)
    if ad is None:
        pass
    return ad

Base.metadata.create_all(engine)


class AdView(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(session, ad_id)
            if ad is None:
                pass
            return jsonify({'article': ad.article})

    def post(self):
        article = request.json['article']
        text = request.json['text']
        owner = request.json['owner']
        with Session() as session:
            ad = Ad(article=article, text=text, owner=owner)
            session.add(ad)
            session.commit()
            return jsonify({'id': ad.id})

    def patch(self, ad_id: int):
        json_data = request.json

        with Session() as session:
            ad = get_ad(session, ad_id)
            if json_data.get('article'):
                ad.article = json_data['article']
            if json_data.get('text'):
                ad.text = json_data['text']
            if json_data.get('owner'):
                ad.owner = json_data['owner']
            session.add(ad)
            session.commit()
            return {
                'article': ad.article,
                'text': ad.text,
                'owner': ad.owner
            }

    def delete(self, ad_id: int):
        with Session() as session:
            ad = get_ad(session, ad_id)
            session.delete(ad)
            session.commit()
            return {
                'status': 'Объявление удалено'
            }


ad_view = AdView.as_view('ads')
app.add_url_rule('/ads/', view_func=ad_view, methods=['POST'])
app.add_url_rule('/ads/<int:ad_id>', view_func=ad_view, methods=['GET', 'PATCH', 'DELETE'])

app.run()