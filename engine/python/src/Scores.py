
import csv
import os


class Score:
    def __init__(self):
        if not os.path.exists('scores.csv'):
            
            # create the file if doesn't exist
            self.clear()
    
    def clear(self):
        with open('scores.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Score', 'Commit', 'Games_Played', 'Win', 'Loss', 'Nullified', 'Score (%)', 'UnderShoot', 'time_avg_bid', 'time_avg_play', 'time_trump'])
    
    def save(self, scores): # , commit_id, games_played, win_loss_annuled, score, score_percent, overshoot, under_shoot, avg_rt):
        # update sorted list
        print('\n scores got', scores)
        with open('scores.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([round(scores['win'], 3) - round(scores['loss'], 3), scores['commit_id'], scores['games_played'], round(scores['win'], 3), round(scores['loss'], 3), scores['annuled'],  round((scores['win']/scores["games_played"])*100, 3), round(scores['under_shoot'], 3), round(scores['response_time_avg_bid'], 3), round(scores['response_time_avg_play'], 3), round(scores['response_time_trump_set'],3)])
        
        self.sort_scores()  # sort the scores
    
    def get(self, commit_id = None):
        rows = []
        if commit_id != None:
            return [row for row in reader if row if row[1] == commit_id]
        with open('scores.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        
        return rows
    def display(self):
        # display in formatted tabular form
        # Open the CSV file
        with open('scores.csv', 'r') as file:
            # Create a CSV reader
            reader = csv.reader(file)

            # Iterate over the rows of the file
            print("\n\t\t\t\t\t\t\t\t--------------------------------- ")
            print("\t\t\t\t\t\t\t\t\t SCORE BOARD")
            print("\t\t\t\t\t\t\t\t--------------------------------- ")
            for row in reader:
                # Print each row as a table row
                print(f"{row[0]:<13} {row[1]:<13} {row[2]:<13} {row[3]:<13} {row[4]:<13} {row[5]:<13} {row[6]:<13} {row[7]:<13} {row[8]:<13} {row[9]:<13} {row[10]:<13}")

    def sort_scores(filename="scores.csv"):
            # Read the contents of the file into a list of rows
            with open("scores.csv", 'r') as input_csv:
                reader = csv.reader(input_csv)
                rows = list(reader)

            # Skip the header row
            header = rows[0]
            data = rows[1:]

            # Sort the data by the second column
            data = sorted(data, key=lambda row: row[0])

            # Write the sorted rows back to the file
            with open("scores.csv", 'w', newline='') as output_csv:
                writer = csv.writer(output_csv)
                writer.writerow(header)
                writer.writerows(data)
if __name__ == '__main__':
    s=Score()
    s.save({'win': 1, 'loss': 0, 'annuled': 0, 'commit_id': '1234', 'games_played': 1, 'response_time_avg': 100, 'under_shoot': 0})
    s.save({'win': 1, 'loss': 0, 'annuled': 0, 'commit_id': '1234', 'games_played': 1, 'response_time_avg': 100, 'under_shoot': 0})
    s.save({'win': 1, 'loss': 0, 'annuled': 0, 'commit_id': '1234', 'games_played': 1, 'response_time_avg': 100, 'under_shoot': 0})
    print(s.get())


'''
    Rank : By Scores
    Commit : commit_id message
    Games Played : No. of games played
    Win/Loss/Nullified : No. of games won/lost/annuled
    Score = win - loss
    Score (%) = (win/total_games_played)*100%
    UnderShoot : sum(bid - score)
    Date : Date of the game
    Avg R.T (ms) : Average reaction time in milliseconds
'''
