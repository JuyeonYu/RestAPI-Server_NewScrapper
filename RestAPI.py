from flask_restful import Resource, reqparse
from flask_restful.representations import json
from DataBaseManager import DatabaseManager
from flask import Flask, jsonify

db = DatabaseManager('54.180.119.242', 'johnny', 'qwas8800', 'newScrapper')

class MainKeyword(Resource):
    # 메인키워드 테이블 CRUD
    
    # C
    # 1. 사용자의 키워드 등록
    # 다음의 4번의 쿼리가 필요함
    # 1. 키워드 테이블에 키워드를 등록
    # 2. 1에서 등록한 키워드의 인덱스를 얻음
    # 3. 2,3에서 얻은 인덱스를 유저_키워드 테이블에 저장

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('idx_user', type=str)
        parser.add_argument('keyword', type=str)

        args = parser.parse_args()
        idx_user = args['idx_user']
        keyword = args['keyword']

        # if user_id and main_keyword:
        sql1 = f"insert into mainKeyword (keyword) value ('{keyword}')"
        db.curs.execute(sql1)
        db.conn.commit()

        sql2 = f"select idx from mainKeyword where keyword = '{한샘}'"
        db.curs.execute(sql2)
        row = db.curs.fetchone()
        idx_keyword = row[0]

        sql3 = f"insert into user_mainKeyword (idx_user, idx_keyword) values ({idx_user},{idx_keyword})"
        db.curs.execute(sql3)
        db.conn.commit()

    # R
    # 1. 사용자의 메인키워드(들) 조회
    # 다음의 1번의 조인 쿼리가 필요함
    # 1. 키워드_유저 테이블과 키워드 테
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str)
        args = parser.parse_args()
        user_id = args['userid']

        if user_id :
            # sql = f"# select idx from user where id ='{user_id}'"
            sql = f"select keyword, idx_keyword from mainKeyword mk, `user` u , user_mainKeyword umk " \
                f"where mk.idx  = umk.idx_keyword " \
                f"and u.id  = '{user_id}'"
            db.curs.execute(sql)

            keys = []
            for column in db.curs.description:
                keys.append(column[0])
            key_number = len(keys)

            json_data = []
            for row in db.curs.fetchall():
                item = dict()
                for q in range(key_number):
                    item[keys[q]] = row[q]
                json_data.append(item)
            data = jsonify(json_data)

            if data is None:
                return ''
            else:
                return data
        else:
            return '{error: userID or mainKeyword parameter null}'

    # U
    # 메인키워드 수정 불가
    def put(self):
        return {'update': 'not supported'}

    # D
    # 1. 사용자의 메인키워드 삭제
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('idx_keyword', type=str)

        args = parser.parse_args()
        idx_keyword = args['idx_keyword']

        if idx_keyword:
            sql = f"delete from user_mainKeyword where idx_keyword = {idx_keyword}"
            db.curs.execute(sql)
            db.conn.commit()
            row = db.curs.fetchall()

            if not row:
                return '{code: 1}'  # success
            else:
                return row
        else:
            return '{error: userID or mainKeyword parameter null}'


class SubKeyword(Resource):
    #서브키워드 테이블 CRUD
    # 필요한 파라미터: 유저아이디, 메인키워드, 서브키워드(unique)

    # C
    # 1. 사용자의 서브키워드 등록
    # 필요: 유저아이디, 메인키워드, 서브키워드

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str)
        parser.add_argument('main', type=str)
        parser.add_argument('sub', type=str)

        args = parser.parse_args()
        user_id = args['userid']
        main_keyword = args['main']
        sub_keyword = args['sub']

        if user_id and main_keyword:
            # sql = f"insert into subKeyword (userid, main, sub) values ('{user_id}', '{main_keyword}', '{sub_keyword}')"
            sql = f"insert into subKeyword(main, sub, userid) select '{main_keyword}', '{user_id}', '{sub_keyword}' from DUAL where not EXISTS(select sub from subKeyword where userid = '{user_id}' and main = '{main_keyword}' and sub = '{sub_keyword}')"
            db.curs.execute(sql)
            db.conn.commit()
            row = db.curs.fetchall()

            if not row:
                return '{code: 1}'  # success
            else:
                return row

    # R
    # 1. 사용자의 서브키워드 조회
    # 필요: 유저아이디, 메인케워드

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str)
        parser.add_argument('main', type=str)

        args = parser.parse_args()
        user_id = args['userid']
        main_keyword = args['main']

        print(user_id, main_keyword)

        if user_id and main_keyword:
            # sql = f"select sub from mainKeyword right join subKeyword on mainKeyword.main = subKeyword.main where subKeyword.main = '{mainKeyword}' and userID ='{userID}'"
            sql = f"select sub from subKeyword where userid = '{user_id}' and main = '{main_keyword}'"
            db.curs.execute(sql)
            db.conn.commit()
            rows = [item[0] for item in db.curs.fetchall()]

            if rows is None:
                return ''
            else:
                return rows
        else:
            return '{error: userID or mainKeyword parameter null}'

    # U
    # 1. 사용자의 서브키워드 수정
    # 필요: 유저아이디, 메인키워드, 서브키워
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str)
        parser.add_argument('main', type=str)
        parser.add_argument('sub', type=str)
        parser.add_argument('newSub', type=str)

        args = parser.parse_args()
        user_id = args['userid']
        main_keyword = args['main']
        sub_keyword = args['sub']
        new_sub_keyword = args['newSub']

        if user_id and main_keyword and sub_keyword:
            print(user_id, main_keyword, sub_keyword, new_sub_keyword)
            sql = f"update subKeyword set sub = '{new_sub_keyword}' where userid = '{user_id}' and main = '{main_keyword}' and sub = '{sub_keyword}'"
            db.curs.execute(sql)
            db.conn.commit()
            rows = [item[0] for item in db.curs.fetchall()]

            if rows is None:
                return ''
            else:
                return rows
        else:
            return '{error: userID or mainKeyword parameter null}'

    # D
    # 1. 사용자의 서브키워드 삭제
    # 필요: 유저아이디, 메인키워드, 서브키워드
    def delete(self):

        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str)
        parser.add_argument('main', type=str)
        parser.add_argument('sub', type=str)

        args = parser.parse_args()
        user_id = args['userid']
        main_keyword = args['main']
        sub_keyword = args['sub']

        if user_id:
            sql = f"delete from subKeyword where userid = '{user_id}' and main = '{main_keyword}' and sub = '{sub_keyword}'"
            db.curs.execute(sql)
            db.conn.commit()
            row = db.curs.fetchall()

            if not row:
                return '{code: 1}'  # success
            else:
                return row
        else:
            return '{error: userID or mainKeyword parameter null}'