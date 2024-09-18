from insert_data.InsertData import InsertData
def main():
    json_file = '/Users/uicheol_hwang/Sever-Model/data/insert_data/test_data.json'

    data_insert = InsertData(json_file)
    data_insert.main()


if __name__ == '__main__':
    main()