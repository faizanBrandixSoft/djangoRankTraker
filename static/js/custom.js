$(document).ready(function () {
    $("#gl,#hl,#deviceSelect,#modeSelect,#gDomain").select2({
        theme: "bootstrap4"
    });

    //
    //
    // $("#rankTrackerForm").on("submit", function (event) {
    //     event.preventDefault();
    //     const formData = $(this).serializeArray();
    //     const data = {};
    //     $.each(formData, function (_, item) {
    //         data[item.name] = item.value;
    //     });
    //
    //     $.ajax({
    //         type: "POST",
    //         url: "http://127.0.0.1:5000/scrape",
    //         contentType: "application/json",
    //         data: JSON.stringify(data),
    //         success: function (response) {
    //             displayResults(response);
    //         },
    //         error: function (xhr, status, error) {
    //             alert("Error: " + status);
    //         }
    //     });
    // });
    //
    // function displayResults(response) {
    //     const resultsDiv = $("#results");
    //     resultsDiv.html("<h2>Scraped Results:</h2>");
    //     const resultsList = $("<ul></ul>");
    //     $.each(response.results, function (_, result) {
    //         const listItem = $("<li></li>").text(result.link);
    //         resultsList.append(listItem);
    //     });
    //     resultsDiv.append(resultsList);
    //
    //     const targetUrlResult = $("<p></p>").text("Target URL Position: " + response.target_url_result);
    //     resultsDiv.append(targetUrlResult);
    // }
});
