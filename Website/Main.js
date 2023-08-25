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
  const collection = mongo.db("kenoGameData").collection("GameData");
  var query = {gameNumber: "10"}
  var result = await collection.findOne(query);
  return result
}

async function displayData(result) {
  var gameTime = document.getElementById("gameTime");
  gameTime.innerHTML = "Unknown"
  /*gameTime.innerHTML = result[""] */

  var gameNumber = document.getElementById("gameNumber");
  gameNumber.innerHTML = result["gameNumber"];

  var drawNumbers = document.getElementById("drawNumbers");
  drawNumbers.innerHTML = result["drawNumbers"];

  var multiplier = document.getElementById("multiplier");
  multiplier.innerHTML = result["multiplier"]

  var headTailResult = document.getElementById("headTailResult");
  headTailResult.innerHTML = result["headTailResult"]

  var APICalls = document.getElementById("APICalls");
  APICalls.innerHTML = "39" // Data is not saved yer [Placeholder]

  var timeSpent = document.getElementById("timeSpent");
  timeSpent.innerHTML = "0 Seconds"
}

async function getData() {
  retrieveData(app).then((result) => {
    displayData(result);
  })
}