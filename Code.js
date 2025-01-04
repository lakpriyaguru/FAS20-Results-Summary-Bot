// Central function to route the request
function doGet(e) {
  // Get the function name from the URL parameter (e.g., ?function=fetchData)
  var functionName = e.parameter.function;

  // Call the corresponding function based on the function name
  if (functionName == "getGPA") {
    return getGPA(e);
  } else {
    return ContentService.createTextOutput("Invalid function name").setMimeType(
      ContentService.MimeType.JSON
    );
  }
}

function getGPA(e) {
  // Log the request
  logRequest(e);

  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

  // Get the first sheet by name, e.g., "Sheet1"
  var sheet = spreadsheet.getSheetByName("ALL"); // Replace "Sheet1" with the name of your first sheet

  if (!sheet) {
    // If the sheet does not exist, return an error
    var errorResult = {
      message: "The specified sheet does not exist",
    };
    return ContentService.createTextOutput(
      JSON.stringify(errorResult)
    ).setMimeType(ContentService.MimeType.JSON);
  }

  var data = sheet.getDataRange().getValues();
  var index = e.parameter.index;
  var userID = e.parameter.userID;

  // Loop through data starting from row 2 (index 1), since row 1 contains headers
  for (var i = 1; i < data.length; i++) {
    if (data[i][1] == index) {
      // Index No is in column A (index 0)

      // Create an object to map column headers to their corresponding row values
      var result = {
        status: "success",
        message: "Request was successful",
        index: data[i][1],
        name: data[i][2],
        combA: data[i][3],
        combB: data[i][4],
        credits: data[i][5],
        gpa: data[i][7],
        rank: data[i][8],
      };

      // Return the result as JSON
      return ContentService.createTextOutput(
        JSON.stringify(result)
      ).setMimeType(ContentService.MimeType.JSON);
    }
  }

  // If index number not found, return a message in JSON format
  var notFoundResult = {
    status: "error",
    message: "Index number not found",
  };
  return ContentService.createTextOutput(
    JSON.stringify(notFoundResult)
  ).setMimeType(ContentService.MimeType.JSON);
}

// Function to log requests
function logRequest(e) {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var logSheet = spreadsheet.getSheetByName("RequestLog");

  // Create the log sheet if it doesn't exist
  if (!logSheet) {
    logSheet = spreadsheet.insertSheet("RequestLog");
    logSheet.appendRow(["Timestamp", "UserID", "Request"]);
  }

  // Get the current timestamp
  var timestamp = new Date();

  // Get the user ID and request details
  var userID = e.parameter.userID || "Unknown"; // Replace with a relevant parameter
  var requestDetails = JSON.stringify(e.parameters);

  // Append the log to the sheet
  logSheet.appendRow([timestamp, userID, requestDetails]);
}
