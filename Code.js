// Central function to route the request
function doGet(e) {
  // Get the function name from the URL parameter (e.g., ?function=fetchData)
  var functionName = e.parameter.function;

  // Call the corresponding function based on the function name
  if (functionName == "getSummary") {
    return getSummary(e);
  } else if (functionName == "getDean") {
    return getDean(e);
  } else if (functionName == "getResults") {
    return getResults(e);
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

  log(userID, "getSummary", index);

  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

  var sheet = spreadsheet.getSheetByName("ALL"); // Replace "Sheet1" with the name of your first sheet

  if (!sheet) {
    var errorResult = {
      status: "error",
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
        repeatTot: data[i][24],
        repeatL1: data[i][9],
        repeatL2: data[i][14],
        repeatL3: data[i][19],
      };
      return ContentService.createTextOutput(
        JSON.stringify(result)
      ).setMimeType(ContentService.MimeType.JSON);
    }
  }
  var notFoundResult = {
    status: "error",
    message: "Index number not found",
  };
  return ContentService.createTextOutput(
    JSON.stringify(notFoundResult)
  ).setMimeType(ContentService.MimeType.JSON);
}

// Function to log requests
function log(usedID, requestFunc, variable) {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var logSheet = spreadsheet.getSheetByName("RequestLog");

  // Create the sheet and set headers if it does not exist
  if (!logSheet) {
    logSheet = spreadsheet.insertSheet("RequestLog");
    logSheet.appendRow(["Timestamp", "UserID", "Request", "Variable"]);
  }

  // Ensure headers are correct
  var headers = logSheet.getRange(1, 1, 1, 4).getValues()[0];
  if (
    headers[0] !== "Timestamp" ||
    headers[1] !== "UserID" ||
    headers[2] !== "Request" ||
    headers[3] !== "Variable"
  ) {
    logSheet
      .getRange(1, 1, 1, 4)
      .setValues([["Timestamp", "UserID", "Request", "Variable"]]);
  }

  // Prepare data to append
  var timestamp = new Date();
  var data = [timestamp, usedID, requestFunc, variable];

  // Append data to the sheet
  logSheet.appendRow(data);
}

// function to getDean
function getDean(e) {
  var userID = e.parameter.userID;
  var level = e.parameter.level;

  log(userID, "getDean", level);

  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet;

  // Determine which sheet to use based on the level
  if (level == "1") {
    sheet = spreadsheet.getSheetByName("DEAN_L01");
  } else if (level == "2") {
    sheet = spreadsheet.getSheetByName("DEAN_L02");
  } else if (level == "3") {
    sheet = spreadsheet.getSheetByName("DEAN_L03");
  } else {
    // Handle invalid level
    var errorResult = { status: "error", message: "Invalid level specified" };
    return ContentService.createTextOutput(
      JSON.stringify(errorResult)
    ).setMimeType(ContentService.MimeType.JSON);
  }

  // Handle missing sheet
  if (!sheet) {
    var errorResult = {
      status: "error",
      message: "The specified sheet does not exist",
    };
    return ContentService.createTextOutput(
      JSON.stringify(errorResult)
    ).setMimeType(ContentService.MimeType.JSON);
  }

  // Get all data from the sheet
  var data = sheet.getDataRange().getValues();

  // Prepare a response object to hold all records
  var records = [];
  for (var i = 1; i < data.length; i++) {
    records.push({
      index: data[i][1],
      name: data[i][3],
      // combA: data[i][4],
      combB: data[i][5],
      // credit: data[i][6],
      gpa: data[i][8],
      rank: data[i][9],
    });
  }

  // Return all records as JSON
  var result = {
    status: "success",
    message: "All records retrieved successfully",
    records: records,
  };

  return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(
    ContentService.MimeType.JSON
  );
}

// Function to handle /results endpoint
function getResults(e) {
  var userID = e.parameter.userID; // Retrieve userID if needed for logging
  var index = e.parameter.index; // Index number of the student

  log(userID, "getResults", index); // Log the request

  // Get the active spreadsheet
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

  // Determine the combination sheets based on the student's combination
  var sheetNameA, sheetNameB, name;
  var allSheet = spreadsheet.getSheetByName("ALL");
  if (!allSheet) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: "error", message: "ALL sheet not found" })
    ).setMimeType(ContentService.MimeType.JSON);
  }

  var allData = allSheet.getDataRange().getValues();
  for (var i = 1; i < allData.length; i++) {
    if (allData[i][1] == index) {
      name = allData[i][2];
      sheetNameA = allData[i][3]; // Assuming combination A is in the 4th column
      sheetNameB = allData[i][4]; // Assuming combination B is in the 5th column
      break;
    }
  }

  if (!sheetNameA || !sheetNameB) {
    return ContentService.createTextOutput(
      JSON.stringify({
        status: "error",
        message: "Index number not found in ALL sheet",
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }

  // Retrieve data from the specified combination sheets
  var sheetA = spreadsheet.getSheetByName(sheetNameA);
  var sheetB = spreadsheet.getSheetByName(sheetNameB);

  if (!sheetA || !sheetB) {
    return ContentService.createTextOutput(
      JSON.stringify({
        status: "error",
        message:
          "Combination sheet(s) not found: " +
          (sheetA ? "" : sheetNameA) +
          (sheetB ? "" : ", " + sheetNameB),
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }

  // Retrieve module mapping
  var moduleSheet = spreadsheet.getSheetByName("Module_Details");
  if (!moduleSheet) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: "error", message: "Modules sheet not found" })
    ).setMimeType(ContentService.MimeType.JSON);
  }

  var moduleData = moduleSheet.getDataRange().getValues();
  var moduleMap = {};
  for (var i = 1; i < moduleData.length; i++) {
    moduleMap[moduleData[i][0]] = moduleData[i][1]; // Assuming 1st column is code, 2nd is name
  }

  var dataA = sheetA.getDataRange().getValues();
  var headersA = dataA[0]; // First row contains subject names

  var dataB = sheetB.getDataRange().getValues();
  var headersB = dataB[0]; // First row contains subject names

  // Define included columns for each combination
  var includeColumnsA = defineColumns(sheetNameA);
  var includeColumnsB = defineColumns(sheetNameB);

  var result = {
    status: "success",
    message: "Request was successful",
    index: index,
    name: name,
    totalSubjects: 0,
    subjects: [],
  };

  // Aggregate results from Sheet A
  for (var i = 1; i < dataA.length; i++) {
    if (dataA[i][0] == index) {
      for (var j = 1; j < headersA.length; j++) {
        if (includeColumnsA.includes(j)) {
          var code = headersA[j];
          result.subjects.push({
            subject: code,
            name: moduleMap[code] || "Unknown",
            grade: dataA[i][j],
          });
        }
      }
      break; // Stop searching once the index is found
    }
  }

  // Aggregate results from Sheet B
  for (var i = 1; i < dataB.length; i++) {
    if (dataB[i][0] == index) {
      for (var j = 1; j < headersB.length; j++) {
        if (includeColumnsB.includes(j)) {
          var code = headersB[j];
          result.subjects.push({
            subject: code,
            name: moduleMap[code] || "Unknown",
            grade: dataB[i][j],
          });
        }
      }
      break; // Stop searching once the index is found
    }
  }

  result.totalSubjects = result.subjects.length; // Calculate total subjects

  return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(
    ContentService.MimeType.JSON
  );
}

// Helper function to define included columns based on sheet name
function defineColumns(sheetName) {
  if (sheetName === "JM_1A") {
    return [1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16];
  } else if (sheetName === "JM_1B") {
    return [1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15];
  } else if (sheetName === "JM_2A") {
    return [1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18];
  } else if (sheetName === "JM_2B") {
    return [1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 19];
  } else if (sheetName === "JM_3B") {
    return [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 17, 18];
  } else if (sheetName === "JM_3C") {
    return [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16];
  } else if (sheetName === "JM_4A") {
    return [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16];
  } else if (sheetName === "JM_4B") {
    return [1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18];
  } else if (sheetName === "JM_4C") {
    return [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 17, 18];
  } else if (sheetName === "GEN_1A") {
    return [2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18];
  } else if (sheetName === "GEN_1B") {
    return [2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17];
  } else if (sheetName === "GEN_1C") {
    return [2, 3, 4, 5, 6, 11, 12, 13, 14, 15];
  } else if (sheetName === "GEN_2A") {
    return [];
  } else if (sheetName === "GEN_2C") {
    return [2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18];
  } else if (sheetName === "GEN_3A") {
    return [2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18];
  } else if (sheetName === "GEN_3B") {
    return [2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19];
  } else if (sheetName === "GEN_3C") {
    return [2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 19];
  } else if (sheetName === "SP_CMIS") {
    return [2, 3, 4, 5, 6, 11, 12, 13, 14, 15];
  } else if (sheetName === "SP_ELTN") {
    return [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16, 17, 18, 19, 20, 21, 22];
  } else if (sheetName === "SP_IMGT") {
    return [2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18];
  } else if (sheetName === "SP_MMST") {
    return [2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16];
  } else if (sheetName === "COMB_1") {
    return [
      1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 24, 25, 26, 27, 28,
      29, 34, 35, 36, 37, 38, 39, 40, 41,
    ];
  } else if (sheetName === "COMB_2") {
    return [
      1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 24, 25, 26, 27, 28,
      29, 30, 35, 36, 37, 38, 39, 40, 41, 42, 43,
    ];
  } else if (sheetName === "COMB_3") {
    return [
      1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 24, 25, 26, 27, 28,
      29, 30, 35, 36, 37, 38, 39, 40,
    ];
  }
  return [];
}
