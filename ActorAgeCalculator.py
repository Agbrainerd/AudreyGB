import requests
import json
import datetime

def dateFormatter(date):
  monthArray = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  splitDate = date.split("-")
  splitYear = int(splitDate[0])
  splitMonth = int(splitDate[1])
  splitDay = int(splitDate[2])
  formattedDate = monthArray[int(splitMonth - 1)] + " " + str(splitDay) + "," + " " + str(splitYear)
  return formattedDate

def movieOrShow():
  mediaTypeInput = input("Would you like to search for a film or a TV show? ")
  if mediaTypeInput in ["film", "movie", "video"]:
    mediaSelected = "movie"
  else:
    mediaSelected = "tv"
  return mediaSelected 

def matchMovie(mediaTypeInput):
  if mediaTypeInput == "movie":
    mediaTypeInquiry = "movie"
    mediaTypeUsed = "movie"
  else:
    mediaTypeInquiry = "tv show"
    mediaTypeUsed = "tv"
  inputAskString = "What is the name of the {} that you would like to search for? " .format(mediaTypeInquiry)
  searchString = input(inputAskString)
  url = "https://api.themoviedb.org/3/search/{}?query={}&include_adult=false&language=en-US&page=1" .format(mediaTypeUsed ,searchString)

  headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMjY3NjAyZTYyZjA4MjRkNjdhYzlkZmJhMTFkOTk3NyIsInN1YiI6IjY1ODAwMGI5MjI2YzU2MDg1OTlkZGEyZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mKUSX-AV7Bp1AbOhwaTHvDWgsfoEi0B-N9RZsfYNdlE"
  }
  isMatch = False
  foundMovie = ""
  indexCount = 0
  response = requests.get(url, headers=headers)
  pythonDict = json.loads(response.text)
  try:
    while not isMatch:
      print("")
      if mediaTypeUsed == "movie":
        print(pythonDict["results"][indexCount]["original_title"] + "      " + pythonDict["results"][indexCount]["release_date"] + ":")
        dateFound = pythonDict["results"][indexCount]["release_date"]
      if mediaTypeUsed == "tv":
        print(pythonDict["results"][indexCount]["original_name"] + "      " + pythonDict["results"][indexCount]["first_air_date"] + ":")
        dateFound = pythonDict["results"][indexCount]["first_air_date"]
      print(pythonDict["results"][indexCount]["overview"])
      print("")
      verifyMatch = input("Is this the " + mediaTypeInquiry + " you were searching for? Press b to go back or x to quit: ")
      if verifyMatch.lower() in ["y", "yes", "true"]:
        isMatch = True
        foundMovie = pythonDict["results"][indexCount]["id"]
      elif verifyMatch.lower() in ["b", "back", "prev", "last"] and indexCount > 0:   
        indexCount -= 2
      elif verifyMatch.lower() in ["b", "back", "prev", "last"] and indexCount == 0:
        print("")
        print("First result is already displayed. Unable to go back. Displaying first result again:")  
        indexCount -= 1
      elif verifyMatch.lower() in ["q", "quit", "x", "exit"]:
        print("Program aborted.")
        print("")
        quit()
      indexCount += 1 
  except:
    print("An error has been encountered and the program must close. Please try again later.")
    print("")
  return foundMovie, dateFound, mediaTypeInquiry

def getCredits(mediaSelected, movieID):
  print("")
  import requests
  url = "https://api.themoviedb.org/3/{}/{}/credits?language=en-US" .format(mediaSelected, movieID)
  headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMjY3NjAyZTYyZjA4MjRkNjdhYzlkZmJhMTFkOTk3NyIsInN1YiI6IjY1ODAwMGI5MjI2YzU2MDg1OTlkZGEyZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mKUSX-AV7Bp1AbOhwaTHvDWgsfoEi0B-N9RZsfYNdlE"
  }
  response = requests.get(url, headers=headers)
  creditStringFormatted = json.loads(response.text) 
  for member in creditStringFormatted["cast"]:
    print("Actor: " + member["name"] + "  Character: " + member["character"])
    yesOrNo = input("Is this the actor you were looking for? ")
    if yesOrNo in ["y", "yes"]:
      actorID = member["id"]
      print("")
      break
    print("")
  return actorID

def getBirthdate(actorID):
  import requests
  url = "https://api.themoviedb.org/3/person/{}?language=en-US" .format(actorID)
  headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMjY3NjAyZTYyZjA4MjRkNjdhYzlkZmJhMTFkOTk3NyIsInN1YiI6IjY1ODAwMGI5MjI2YzU2MDg1OTlkZGEyZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mKUSX-AV7Bp1AbOhwaTHvDWgsfoEi0B-N9RZsfYNdlE"
  }
  response = requests.get(url, headers=headers)
  pythonDictionary = json.loads(response.text)
  print(pythonDictionary["biography"])
  return(pythonDictionary["birthday"])

runAgain = True
while runAgain == True:
  try:
    monthArray = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    showOrMovieChoice = movieOrShow()
    movieID = matchMovie(showOrMovieChoice)
    actorID = getCredits(showOrMovieChoice, movieID[0])
    birthdayOut = getBirthdate(actorID)
    filmOrShow = movieID[2]

    #String/Text Processing Stuff
    birthdaySplit = birthdayOut.split("-")
    testYear = int(birthdaySplit[0])
    testMonth = int(birthdaySplit[1])
    testDay = int(birthdaySplit[2])

    currentTime = str(datetime.datetime.now())
    currentTimeSplit = currentTime.split("-")
    currentYear = int(currentTimeSplit[0])
    currentMonth = int(currentTimeSplit[1])
    currentDay = int(currentTimeSplit[2][:2])

    thenTimeSplit = movieID[1].split("-")
    thenYear = int(thenTimeSplit[0])
    thenMonth = int(thenTimeSplit[1])
    thenDay = int(thenTimeSplit[2])
    
    #These blocks are for calculating ages
    age = currentYear - testYear
    if currentMonth < testMonth:
      age = age - 1
    if currentMonth == testMonth:
      if currentDay < testDay:
        age = age - 1    

    ageThen = thenYear - testYear
    if thenMonth < testMonth:
      ageThen = ageThen - 1
    if thenMonth == testMonth:
      if thenDay < testDay:
        ageThen = ageThen - 1     
    #Display Stuff
    print("")
    print("The actor's date of birth is", monthArray[int(testMonth - 1)], str(testDay) + ",", str(testYear) + ".")
    print("The actor is currently", age, "years old.")
    print("The", filmOrShow, "was released", dateFormatter(movieID[1]))
    print("When the", filmOrShow, "was released the actor was", ageThen, "years old.")

  except:
    print("The program has encountered an error and must close.")
    print("")
  print("")
  runAgainInput = input("Would you like to run the program again? ")
  if runAgainInput.lower() in ["y", "yes", "sure", "okay"]:
    runAgain = True
    print("")
  else:
    runAgain = False
