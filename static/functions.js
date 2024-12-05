function setState(currentDate, guess, difference) {
  let values = JSON.parse(localStorage.getItem("game-state"));
  if (values) {
    if (values[currentDate].length < 6) {
      values[currentDate].push({ guess: guess, closeness: difference });
    }
  } else {
    values = { currentDate: [] };
  }
  localStorage.setItem("game-state", JSON.stringify(values));
}
