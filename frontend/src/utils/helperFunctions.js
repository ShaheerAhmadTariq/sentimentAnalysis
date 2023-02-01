// Function to sort date according to timestamp
const dateSort = (datesArray) => {
  let Dates = datesArray;
  let options = { month: "short", day: "numeric" };

  Dates = Dates.map((elm) => {
    return new Date(elm);
  }).sort();

  Dates = Dates.sort((a, b) => a < b).map((elm) =>
    elm.toLocaleDateString("en-US", options)
  );
  return Dates;
};

// Function to get values from array of objects
function getArrayOfObjectValues(array) {
  return array.map((item) => Object.entries(item)[0][1]);
}

// Function to get keys from array of objects
function getArrayOfObjectKeys(array) {
  return array.map((item) => Object.entries(item)[0][0]);
}
export { dateSort, getArrayOfObjectValues, getArrayOfObjectKeys };
