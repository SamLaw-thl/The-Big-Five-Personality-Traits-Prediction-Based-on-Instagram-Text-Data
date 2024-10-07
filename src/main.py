import instaloader_function as ig
import database as db
import personality_prediction_model as bp
import personality_graph as pg


def main() -> None:
    """
    Main function for interacting with the Instagram data pipeline and personality prediction.
    """
    while True:
        db.create_table()
        L = ig.initialize_instaloader()
        print("1. Fetch Instagram Data")
        print("2. Print all the instagram users stored in the database")
        print("3. Personality Prediction")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Please enter your Instagram username: ")
            password = input("Please enter your Instagram password: ")
            ig.instagram_login(L, username, password)

            target_username = input("Please enter target instagram username: ") # e.g. taylorswift avrillavigne adele 
            profile = ig.target_name_input(L, target_username)
            db.insert_user_profile_table(profile)
            db.insert_post_table(profile)

        elif choice == '2':
            db.print_all_username()

        elif choice == '3':
            target_username = input("Please enter target instagram username: ")

            if db.is_in_the_database(target_username):
                profile = ig.target_name_input(L, target_username)
                personality_prediction = bp.personality_detection_microsoft_finetuned(profile)
            
                chart_option = input("Enter 0 to select bar chart or enter 1 to select rader chart to visualize the prediction: ")
                if chart_option == '0':
                    pg.personality_bar_chart(personality_prediction)
                elif chart_option == '1':
                    pg.personality_rader_chart(personality_prediction)
                else:
                    print("invalid input! ")
            else:
                print("Input username is not in the database")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invaid option. Please try again")


if __name__ == '__main__':
    main()