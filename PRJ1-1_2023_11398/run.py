import os
from lark import Lark, Transformer, UnexpectedInput

class MyTransformer(Transformer):
    def print_query(self, query_name):
        # query에 따른 올바른 출력을 만드는 함수
        print(f'DB_2023-11398> \'{query_name}\' requested')

    def create_table_query(self, items):
        self.print_query('CREATE TABLE')

    def select_query(self, items):
        self.print_query('SELECT')

    def drop_table_query(self, items):
        self.print_query('DROP TABLE')

    def explain_query(self, items):
        self.print_query('EXPLAIN')

    def describe_query(self, items):
        self.print_query('DESCRIBE')

    def desc_query(self, items):
        self.print_query('DESC')

    def show_tables_query(self, items):
        self.print_query('SHOW TABLES')

    def delete_query(self, items):
        self.print_query('DELETE')

    def insert_query(self, items):
        self.print_query('INSERT')

    def update_query(self, items):    
        self.print_query('UPDATE')
        
    def EXIT(self, items):
        quit()

# 절대 경로를 사용해서 grammar 파일이 존재하면 실행되도록 하기
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grammar_path = os.path.join(script_dir, 'grammar.lark')
    with open(grammar_path, 'r') as file:
        sql_parser = Lark(file.read(), start="command", lexer="basic")

except FileNotFoundError:
    print(f"Error: 'grammar.lark' file not found in {script_dir}")

# 사용자의 입력을 받는 함수
def Reading():
    # 사용자가 입력한 한 줄 혹은 여러줄의 query input을 읽기
    total_input = []

    # 연속적으로 input을 받을 때, 세미콜론이 마지막에 나오면 끝나도록
    NotEnd = True

    while NotEnd:
        # 사용자의 입력을 받고 앞뒤의 공백을 제거
        query_input = input('DB_2023-11398> ').strip()
        
        # 입력받는 query line을 total_input에 저장
        total_input.append(query_input)

        # 세미콜론으로 끝날 경우 입력 값을 받는 것을 중단
        if query_input.endswith(';'):
            NotEnd = False

    # 여러번 입력받아 쪼개진 input을 한 줄로 결합
    total_line = ' '.join(total_input)

    # 한 줄로 만든 input을 세미콜론을 기준으로 여러 query로 분리
    separated_line = total_line[:-1].split(';')
    queryList = map(lambda each_query : each_query + ';', separated_line)

    return queryList

# 입력 받은 input을 하나씩 파싱하는 함수
def Parsing(sql_parser, queryList, notError):
    for query in queryList:
        if (notError):
            try:
                # query를 하나씩 파싱
                parsed_tree = sql_parser.parse(query)

                # 파싱한 값을 transform해서 함수를 출력함수를 실행
                MyTransformer().transform(parsed_tree)
            
            # 파싱이 실패하면 Syntax error 출력
            except UnexpectedInput:
                # 여러줄 입력시 query sequence 중간에 에러가 있을 경우 중단
                notError = False
                print('DB_2023-11398> Syntax error')

while True:
    # query sequence 중간에 에러가 있을 경우 중단하는 역할
    # 입력을 새로 받을 때 다시 초기화
    notError = True

    # 사용자가 입력한 query input 읽기
    queryList = Reading()

    # 입력 받은 query list를 파싱
    Parsing(sql_parser, queryList, notError)

