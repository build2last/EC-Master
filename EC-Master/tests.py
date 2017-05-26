import settings

def test_category_func():
    from Category import CategoryApi
    print(len(CategoryApi.get_level_3_nodes("JD")))
    print(len(CategoryApi.get_level_3_nodes("TMALL")))
    print(len(CategoryApi.get_level_3_nodes("AMZ")))
    CategoryApi.plant_trees() # 解析出商品目录树存储在本地，我称之为种树

def test_dataparser_func():
    from DataParser import jsonToDataBase
    json_path = settings.json_dir_path
    jsonToDataBase.load_json_from_dir_to_mdb(json_path)

def main():
    test_category_func()
    test_dataparser_func()

if __name__ == '__main__':
    main()