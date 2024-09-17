from config.InsertData import InsertData
def main():
    json_file = '/Users/uicheol_hwang/Sever-Model/api/config/test_data.json'

    data_insert = InsertData(json_file)
    data_insert.main()


if __name__ == '__main__':
    main()