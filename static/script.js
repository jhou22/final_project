function setState(currentDate, guess, difference, logged_in, actual_price) {
  const alphabet = {
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six'
  }
  const difference_conversion = {
    'lower close': 'A tiny bit too low',
    'upper close': 'A tiny bit too high',
    'lower far': 'Way too low',
    'upper far': 'Way too high',
    'exact': 'Correct'
  }
  const account_guesses = JSON.parse(document.getElementById('account_guesses').textContent)
  let values = JSON.parse(localStorage.getItem("game-state"))
  let gameStatus = localStorage.getItem("game-status")
  if (!gameStatus) {
    localStorage.setItem('game-status', 'UNKNOWN')
  }
  // if logged into account, then just get the values from account and just return
  if (logged_in == 'True') {
    console.log("Logged in")
    localStorage.clear()
    values = JSON.parse(localStorage.getItem("game-state"))
    for (let i = 0; i < account_guesses.length; i++) {
      // console.log(account_guesses[i].difference)
      document.getElementById(`guess${alphabet[i + 1]}`).innerText = account_guesses[i].guess
      document.getElementById(`guess${alphabet[i + 1]}-status`).innerText = difference_conversion[account_guesses[i].closeness]
      if (values) { // always guaranteed to be the first value
        values[currentDate].push({ guess: account_guesses[i].guess, difference: account_guesses[i].closeness })
      } else {
        values = { [currentDate]: [{ guess: account_guesses[i].guess, difference: account_guesses[i].closeness }] };
      }
      if (account_guesses[i].closeness == 'exact') { // guaranteed to be the last value in guess
        gameStatus = "WIN"
      }
      if (account_guesses.length >= 6 && account_guesses[5].closeness != 'exact') {
        gameStatus = "LOSE"
      }
    }
    localStorage.setItem("game-state", JSON.stringify(values));
    localStorage.setItem("game-status", gameStatus)
    if (localStorage.getItem("game-status") == "LOSE") {
      document.getElementById('game-status').innerText = `You Lost! The correct answer was ${actual_price}`
    }
    
    if (localStorage.getItem("game-status") == "WIN") {
      document.getElementById('game-status').innerText = `You Win! The correct answer was ${actual_price}`
    }

    if (localStorage.getItem("game-status") == "UNKNOWN") {
      document.getElementById('game-status').innerText = ''
    }
    return
  }
  if (values && values !== 'undefined' && values[currentDate] !== 'undefined') {
    console.log(gameStatus !== 'WIN')
    if (values[currentDate].length < 6 && guess !== 'None' && difference !== 'None' && (gameStatus != 'WIN' && gameStatus != 'LOSE')) {
      if (difference == 'exact') {
        localStorage.setItem("game-status", 'WIN')
      }
      values[currentDate].push({ guess: guess, difference: difference });
      if (values[currentDate].length >= 6 && difference != 'exact') {
        localStorage.setItem("game-status", "LOSE")
      }
    }
  } else {
    values = { [currentDate]: [] };
    localStorage.setItem("game-state", JSON.stringify(values));
    localStorage.setItem("game-status", "UNKNOWN");
    return
  }
  // not logged in case
  if (gameStatus == "WIN") {
    for (let i = 0; i < values[currentDate].length; i++) {
      // console.log(`i = ${i}, ${values[currentDate][i].guess}`)
      document.getElementById(`guess${alphabet[i + 1]}`).innerText = values[currentDate][i].guess
      document.getElementById(`guess${alphabet[i + 1]}-status`).innerText = difference_conversion[values[currentDate][i].difference]
    }
    localStorage.setItem("game-state", JSON.stringify(values));
    localStorage.setItem("game-status", "WIN")
    document.getElementById('game-status').innerText = `You Win! The correct answer was ${actual_price}`
    return
  }
  console.log("Moving on")
  if (gameStatus == "LOSE") {
    for (let i = 0; i < values[currentDate].length; i++) {
      // console.log(`i = ${i}, ${values[currentDate][i].guess}`)
      document.getElementById(`guess${alphabet[i + 1]}`).innerText = values[currentDate][i].guess
      document.getElementById(`guess${alphabet[i + 1]}-status`).innerText = difference_conversion[values[currentDate][i].difference]
    }
    localStorage.setItem("game-state", JSON.stringify(values));
    localStorage.setItem("game-status", "LOSE")
    document.getElementById('game-status').innerText = `You Lost! The correct answer was ${actual_price}`
    return
  }
  // hasn't won or lost yet
  
  for (let i = 0; i < values[currentDate].length; i++) {
    // console.log(`i = ${i}, ${values[currentDate][i].guess}`)
    document.getElementById(`guess${alphabet[i + 1]}`).innerText = values[currentDate][i].guess
    document.getElementById(`guess${alphabet[i + 1]}-status`).innerText = difference_conversion[values[currentDate][i].difference]
  }
  localStorage.setItem("game-state", JSON.stringify(values));
  if (localStorage.getItem("game-status") == "LOSE") {
    document.getElementById('game-status').innerText = `You Lost! The correct answer was ${actual_price}`
  }
  
  if (localStorage.getItem("game-status") == "WIN") {
    document.getElementById('game-status').innerText = `You Win! The correct answer was ${actual_price}`
  }

  if (localStorage.getItem("game-status") == "UNKNOWN") {
    document.getElementById('game-status').innerText = ''
  }
}
