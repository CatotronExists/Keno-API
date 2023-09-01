const app = new Realm.App({ id: "data-wlrnc" });
const apiKey = ""

async function login(apiKey) {
  // Create an API Key credential
  const credentials = Realm.Credentials.apiKey(apiKey);
  // Authenticate the user
  const user = await app.logIn(credentials);
  // `App.currentUser` updates to match the logged in user
  console.assert(user.id === app.currentUser.id);
  return user
}

/* allow to sign in with API Key*/

async function retrieveData(app) {
  await login(apiKey)
  const mongo = app.currentUser.mongoClient("KenoDataVis");
  // Get Game Stats
  const gameCollection = mongo.db("kenoGameData").collection("GameData");
  let gameResult = await gameCollection.aggregate([
    {
      '$sort': {
        'timestamp': -1
      }
    }, {
      '$limit': 1
    }
  ])
  // Get Stats
  /*const statsCollection = "placeholder"
  let stats = .aggregate*/

  return gameResult//, stats
}

async function displayData(gameResult) {
  let gameTime = document.getElementById("gameTime");
  gameTime.innerHTML = (gameResult[0].gameTime)

  let gameNumber = document.getElementById("gameNumber");
  gameNumber.innerHTML = (gameResult[0].gameNumber);

  let drawNumbers = document.getElementById("drawNumbers");
  drawNumbers.innerHTML = (gameResult[0].drawNumbers)

  let multiplier = document.getElementById("multiplier");
  console.log(gameResult[0].multiplier)
  if (gameResult[0].multiplier == "1") {
    multiplier.innerHTML = "reg"
  } else {
    multiplier.innerHTML = ("x" + gameResult[0].multiplier)
  }

  let headTailResult = document.getElementById("headTailResult");
  headTailResult.innerHTML = (gameResult[0].headTailResult)

  let APICalls = document.getElementById("APICalls");
  APICalls.innerHTML = "39" // Data is not saved yet [Placeholder]

  let timeSpent = document.getElementById("timeSpent");
  timeSpent.innerHTML = "0 Seconds" // Not setup
}

async function getData() {
  // add await new document then run loop
  retrieveData(app).then((gameResult) => {
    displayData(gameResult).then(updateGrid(gameResult));
  })
} 

function updateGrid(drawNumbers) {
  let rawNumbers = drawNumbers[0].drawNumbers
  let numbers = JSON.parse("[" + rawNumbers + "]");
  numbers.forEach(element => {
    if (element < 41) {
      document.getElementById(element).style.background = "#ff0000"; // Red - Heads
    } else {
      document.getElementById(element).style.background = "#0000ff"; // Blue - Tails
    }
  })
  if (drawNumbers[0].headTailResult == "Heads") {
    document.getElementById("gridSplit").style.background = "#f94141" // Red
    } else if (drawNumbers[0].headTailResult == "Tails") {
      document.getElementById("gridSplit").style.background = "#419ff9" // Blue
    } else if (drawNumbers[0].headTailResult == "Evens") {
      document.getElementById("gridSplit").style.background = "#8841f9" // Purple
    } else {
      document.getElementById("gridSplit").style.background = "#ffffff" // White (error)
    }
}