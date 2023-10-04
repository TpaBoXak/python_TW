from work_with_data import db_manager


def main():
    db_manager.create_investor()
    db_manager.create_team()
    db_manager.create_match()
    db_manager.create_player()
    # db_manager.create_bd()


if __name__ == "__main__":
    print("Start")
    main()
