from service.InsertData import InsertData

def main():
    # JSON 파일 경로 설정 (사용자 환경에 맞게 변경)
    json_file = '/Users/uicheol_hwang/Sever-Model/data/test_data.json'

    # InsertData 인스턴스 생성
    data_insert = InsertData(json_file)

    # 전체 실행 흐름 수행
    data_insert.run()


if __name__ == '__main__':
    main()