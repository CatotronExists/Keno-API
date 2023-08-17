/* Get Data from MongoDB and display in HTML */
/*const { MongoClient } = require("mongodb");*/
function getData()
    {
        /*Get and sort data, then set elements to those values*/

        var gameNumber = document.getElementById("gameNumber");
        gameNumber.innerHTML = 444;

        var drawNumbers = document.getElementById("drawNumbers");
        drawNumbers.innerHTML = "1, 4, 5, 6, 7, 32, 45, 63, 79";

        var multiplier = document.getElementById("multiplier");
        multiplier.innerHTML = "reg"

        var headTailResult = document.getElementById("headTailResult");
        headTailResult.innerHTML = "evens"
    }

