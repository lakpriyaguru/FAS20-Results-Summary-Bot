// Central function to route the request
function doGet(e) {
  // Get the function name from the URL parameter (e.g., ?function=fetchData)
  var functionName = e.parameter.function;

  // Call the corresponding function based on the function name
  if (functionName == "getSummary") {
    return getSummary(e);
  } else if (functionName == "getDean") {
    return getDean(e);
  } else {
    return ContentService.createTextOutput("Invalid function name").setMimeType(
      ContentService.MimeType.JSON
    );
  }
}

// function to getSummary
function getSummary(e) {
  var userID = e.parameter.userID;
  var index = e.parameter.index;

  log(userID, "getGPA", index);

  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

  var sheet = spreadsheet.getSheetByName("ALL"); // Replace "Sheet1" with the name of your first sheet

  if (!sheet) {
    var errorResult = {
      message: "The specified sheet does not exist",
    };
    return ContentService.createTextOutput(
      JSON.stringify(errorResult)
    ).setMimeType(ContentService.MimeType.JSON);
  }

  var data = sheet.getDataRange().getValues();

  for (var i = 1; i < data.length; i++) {
    if (data[i][1] == index) {
      var result = {
        status: "success",
        message: "Request was successful",
        index: data[i][1],
        name: data[i][2],
        combA: data[i][3],
        combB: data[i][4],
        credit: data[i][20],
        gpa: data[i][22],
        rank: data[i][23],
        repeat: data[i][24],
      };
      return ContentService.createTextOutput(
        JSON.stringify(result)
      ).setMimeType(ContentService.MimeType.JSON);
    } else {
      // var notFoundResult = {status: "error", message: "Index number not found",};
      // return ContentService.createTextOutput(JSON.stringify(notFoundResult)).setMimeType(ContentService.MimeType.JSON);
    }
  }
}

// Function to log requests
function log(usedID, requestFunc, index) {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var logSheet = spreadsheet.getSheetByName("RequestLog");

  // Create the sheet and set headers if it does not exist
  if (!logSheet) {
    logSheet = spreadsheet.insertSheet("RequestLog");
    logSheet.appendRow(["Timestamp", "UserID", "Request", "Index"]);
  }

  // Ensure headers are correct
  var headers = logSheet.getRange(1, 1, 1, 4).getValues()[0];
  if (
    headers[0] !== "Timestamp" ||
    headers[1] !== "UserID" ||
    headers[2] !== "Request" ||
    headers[3] !== "Index"
  ) {
    logSheet
      .getRange(1, 1, 1, 4)
      .setValues([["Timestamp", "UserID", "Request", "Index"]]);
  }

  // Prepare data to append
  var timestamp = new Date();
  var data = [timestamp, usedID, requestFunc, index];

  // Append data to the sheet
  logSheet.appendRow(data);
}
