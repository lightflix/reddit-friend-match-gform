import csv

class User:

    def __init__(self, redditUsername, age, gender, ageGroupsInterest, genderInterest, hobbyInterests):
        self.redditUsername = redditUsername

        self.age = age
        self.gender = gender

        self.ageGroupsInterest = ageGroupsInterest
        self.genderInterests = genderInterest
        self.hobbyInterests = hobbyInterests
        self.potential_candidates = []
        self.taken = False

class Matcher:

    def __init__(self, list_of_users):
        self.list_of_users = list_of_users
        self.takenPool = []
        self.matches = []

    def beginMatch(self):

        userListLength = len(self.list_of_users)
        for user_index in range(userListLength):
            for candidate_index in range(userListLength):
                if self.list_of_users[user_index] != self.list_of_users[candidate_index] and self.list_of_users[candidate_index].gender in self.list_of_users[user_index].genderInterests: #self.list_of_users[candidate_index].redditUsername not in self.takenPool:

                    for ageGroup in self.list_of_users[user_index].ageGroupsInterest:
                        if self.list_of_users[candidate_index].age >= ageGroup[0] and self.list_of_users[candidate_index].age <= ageGroup[1]:
                            match_score = (len(list(set(self.list_of_users[user_index].hobbyInterests) & set(self.list_of_users[candidate_index].hobbyInterests)))*100/max(len(self.list_of_users[user_index].hobbyInterests), len(self.list_of_users[candidate_index].hobbyInterests))) - abs((self.list_of_users[user_index].age - self.list_of_users[candidate_index].age))*0.42069
                            self.list_of_users[user_index].potential_candidates.append((self.list_of_users[candidate_index], round(match_score, 3)))
                            break
        
            potentialCandidatesLength = len(self.list_of_users[user_index].potential_candidates)
            if potentialCandidatesLength > 0:
                self.list_of_users[user_index].potential_candidates.sort(key = lambda x:x[1], reverse=True)
                # self.list_of_users[user_index].potential_candidates = self.list_of_users[user_index].potential_candidates[:7]

                for pc_index in range(potentialCandidatesLength):
                    if not (self.list_of_users[user_index].potential_candidates[pc_index][0].taken or self.list_of_users[user_index].taken):
                        self.list_of_users[user_index].potential_candidates[pc_index][0].taken = True
                        self.list_of_users[user_index].taken = True
                        self.matches.append((self.list_of_users[user_index].redditUsername, self.list_of_users[user_index].potential_candidates[pc_index][0].redditUsername, self.list_of_users[user_index].potential_candidates[pc_index][1]))
                        break

        # for user in self.list_of_users:
        #     for potential_candidate in user.potential_candidates:
        #         if potential_candidate in self.takenPool:
                    
        #         else:
        #             self.takenPool.append(potential_candidate)
        #             break

        # for user in self.takenPool:
        #     print(user[0].redditUsername, user[1])

                
        # for user in self.list_of_users:
        #     print(user.redditUsername, "age::",user.age, "::interested in" ,user.ageGroupsInterest, "", user.genderInterests, "\n\tcandidates below::", )
        #     for candidate_tuple in user.potential_candidates:
        #         print(candidate_tuple[0].redditUsername, "(", candidate_tuple[0].age,"", candidate_tuple[0].gender, "--" ,candidate_tuple[1],"%)", end=", \n")
        #     print("\n")

        # for match in self.matches:
        #     print(match)

        # print(len(self.matches))

        # for user in self.list_of_users:
        #     if user.taken == False:
        #         for candidate in user.potential_candidates:
        #             print(user.redditUsername, "tried to match with ", candidate[0].redditUsername, candidate[1])

        self.matches.sort(key = lambda x:x[2], reverse=True)
        return self.matches

class Populater:

    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.usernames = []

    def importData(self):
        with open(self.filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            next(reader)
            for row in reader:
                self.data.append(row)
    
    def populateUsers(self):

        list_of_users = []
        
        for row in self.data:

            redditUsername = row[1].lower()

            if redditUsername not in self.usernames:
                self.usernames.append(redditUsername)

                age = int(row[3])

                if row[2].lower() == "male":
                    gender = "M"
                else:
                    gender = "F"

                ageGroupsInterest = []
                age_range_list = row[4].split(";")
                age_empty = 1

                for age_range_text in age_range_list:
                    if "+" in age_range_text:
                        age_range_lower, age_range_upper = 41, 120
                    else: 
                        age_range_pair = age_range_text.split('-')
                        age_range_lower_raw = int(age_range_pair[0])
                        if age_range_lower_raw == 18 or age_range_lower_raw == 25 or age_range_lower_raw == 30 or age_range_lower_raw == 35 or age_range_lower_raw == 40:
                            age_range_lower = int(age_range_pair[0])+1            
                        else:
                            age_range_lower = age_range_lower_raw
                        age_range_upper = int(age_range_pair[1])
                
                    if age_range_lower >= round(age/2)+7 and round(age_range_upper/2)+6 <= age: 
                        age_empty = 0
                        age_range_tuple = (age_range_lower, age_range_upper)
                        ageGroupsInterest.append(age_range_tuple)

                if age_empty == 1:
                    ageGroupsInterest.append((16,18))        

                hobbyInterests = []
                hobbyInterestsList = row[6].split(";")
                for interest in hobbyInterestsList:
                    hobbyInterests.append(interest)

                genderInterests = []
                
                genderInterestsList = row[5].split(";")
                for interest in genderInterestsList:
                    if (interest == "Only males" or  interest == "Male") and "M" not in genderInterests:
                        genderInterests.append("M")
                    elif (interest == "Only females" or  interest == "Female") and "F" not in genderInterests:
                        genderInterests.append("F")
                    elif len(genderInterests) == 0:
                        genderInterests.append("M")
                        genderInterests.append("F")

                list_of_users.append(User(redditUsername, age, gender, ageGroupsInterest, genderInterests, hobbyInterests))

        return list_of_users

if __name__ == "__main__":
    populater_object = Populater("real.csv")
    populater_object.importData()
    list_of_users = populater_object.populateUsers()

    matcher_object = Matcher(list_of_users)
    matches = matcher_object.beginMatch()

    #write matches to csv file
    header = ["User", "Matches with", "Score %"]

    with open('matches.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for match in matches:
            writer.writerow([match[0], match[1], match[2]])

    print("Matching complete - See output CSV file")