from flask_restful import Resource, reqparse
from DataBaseManager import DatabaseManager


db = DatabaseManager('54.180.88.102', 'johnny', 'qwas8800', 'newScrapper')


class MainKeyword(Resource):

    # 메인키워드 테이블 CRUD
    # 필요한 파라미터: 유저아이디, 메인키워드(unique)

    # C
    # 1. 사용자의 키워드 등록
    # 필요: 유저아이디, 메인키워드
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str)
        parser.add_argument('main', type=str)

        args = parser.parse_args()
        user_id = args['userid']
        main_keyword = args['main']

        if user_id and main_keyword:
            # sql = f"insert into mainKeyword (userid, main) values ('{user_id}', '{main_keyword}')"
            sql = f"insert into mainKeyword(main, userid) select '{main_keyword}', '{user_id}' from DUAL where not EXISTS(select main from mainKeyword where userid = '{user_id}' and main = '{main_keyword}')"
            db.curs.execute(sql)
            db.conn.commit()
            row = db.curs.fetchall()

            if not row:
                return '{code: 1}'  # success
            else:
                return row

    # R
    # 1. 사용자의 메인키워드 조회
    # 필요: 유저아이디
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str)

        args = parser.parse_args()
        user_id = args['userid']

        if user_id :
            # sql = f"select sub from mainKeyword right join subKeyword on mainKeyword.main = subKeyword.main where subKeyword.main = '{mainKeyword}' and userID ='{userID}'"
            sql = f"select main from mainKeyword where userid = '{user_id}'"
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
    # 메인키워드 수정 불가
    def put(self):
        return {'update': 'not supported'}

    # D
    # 1. 사용자의 메인키워드 삭제
    # 필요: 유저아이디, 메인키워드
    #TODO: 서브키워드의 정보를 어떻게 지울지 생각해봐야함

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str)
        parser.add_argument('main', type=str)

        args = parser.parse_args()
        user_id = args['userid']
        main_keyword = args['main']

        if user_id:
            print(user_id, main_keyword)
            sql = f"delete from mainKeyword where userID = '{user_id}' and main = '{main_keyword}'"
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