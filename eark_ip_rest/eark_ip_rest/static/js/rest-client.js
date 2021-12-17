/**
* Document ready function, loaded up on start
*/
$(document).ready(function () {
  /**
  * Event handler for the file selector
  */
  $(':file').on('change', function () {
    // Disable the submit button
    // $('button').prop('disabled', true)
    // Grab the label component
    var fileLabel = $(this).siblings('.custom-file-label')
    // Get filename without the fake path prefix
    var fileName = $(this).val().split('\\').pop()
    // Set the filename selection, a little tricksy
    fileLabel.addClass('selected').html(fileName)
    // Calculate and display the SHA1 of the file
    calcFileSha1(this.files[0])
  })

  $('#frm-validate').submit(function () {
    $('button').prop('disabled', true)
    $('button').text('Processing, please wait.')
    return true
  })
})

/**
* Calculates the SHA-1 of selected file and displays the result
*/
function calcFileSha1 (file) {
  $('button').prop('disabled', true)
  $('input:text').val('Calcluating package checksum...')
  // New checksum calculator instance
  var rusha = new Rusha()
  // File reader to get data
  var reader = new FileReader()
  // Register reader onload event
  reader.onload = function (e) {
    // Calculate the checksum from the reader result
    var digest = rusha.digest(reader.result)
    // Set the label when finished
    $('input:text').val(digest)
    // Enable the submit button
    $('button').prop('disabled', false)
  }
  // Signal checkcum calculation and load reader
  reader.readAsBinaryString(file)
}

function statusSorter (cellA, cellB) {
  const aMatch = getCellText(cellA)
  const bMatch = getCellText(cellB)
  return aMatch.localeCompare(bMatch)
  }

function idSorter (cellA, cellB) {
  var [idStrA, idNumA] = getCellId(cellA)
  var [idStrB, idNumB] = getCellId(cellB)
  const strSort = idStrA.localeCompare(idStrB)
  if (strSort !== 0) {
    return strSort
  }
  return idNumA - idNumB
}

function getCellId (cellContents) {
  const id = getCellText(cellContents)
  return breakId(id)
}
function breakId (id) {
  const idMatch = id.match(/^([^0-9]*)([0-9]*)/m)
  return [idMatch[1], idMatch[2]]
}

function getCellText (cellContents) {
  return cellContents.match(/^.*>(.*)<.*/m)[1]
}
