import os
import csv
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.exc import OperationalError, IntegrityError
from homepageconfig import SQLALCHEMY_DATABASE_URI

# DB 연결 설정
# MySQL은 autocommit=False가 기본이므로 명시적인 커밋이 필요
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
metadata = MetaData()

# AzQuiz 테이블 정의
# MySQL의 AUTO_INCREMENT는 primary_key=True를 Integer 컬럼에 지정하면 자동으로 설정됨
AzQuiz = Table('AzQuiz', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('quiz', String(255)),  # MySQL은 String 타입에 길이를 명시하는 것이 좋음
    Column('answer', String(255)),
    Column('hint', String(255))
)

# 기존 테이블 삭제 및 재생성
try:
    print("기존 AzQuiz 테이블을 삭제합니다 (존재하는 경우).")
    AzQuiz.drop(engine, checkfirst=True)
    metadata.create_all(engine)
    print("새 AzQuiz 테이블이 생성되었습니다.")
except OperationalError as e:
    print(f"테이블 삭제/생성 중 오류 발생: {e}")
except Exception as e:
    print(f"예상치 못한 오류 발생: {e}")

# CSV 경로
csv_path = os.path.join(os.getcwd(), 'utils', 'src', 'azgag_v3.csv')

# 데이터 삽입
data_to_insert = []
try:
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            data_to_insert.append({
                'quiz': row[0],
                'answer': row[1],
                'hint': row[2]
            })
except FileNotFoundError:
    print(f"오류: {csv_path} 파일을 찾을 수 없습니다.")
    exit()

print(f"{len(data_to_insert)}개의 데이터를 읽어왔습니다.")

# 실행 (트랜잭션 커밋 포함)
if data_to_insert:
    with engine.connect() as conn:
        try:
            conn.execute(AzQuiz.insert(), data_to_insert)
            # MySQL에서는 반드시 커밋이 필요합니다.
            conn.commit()
            print("데이터베이스에 퀴즈가 성공적으로 삽입되었습니다.")
        except IntegrityError as e:
            print(f"데이터 삽입 중 무결성 오류 발생: {e}")
            # 트랜잭션 롤백
            conn.rollback()
        except Exception as e:
            print(f"데이터 삽입 중 오류 발생: {e}")
            conn.rollback()
else:
    print("삽입할 데이터가 없습니다.")