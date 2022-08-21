const url = window.location.href //Grap the Url


const quizBox = document.getElementById('quiz-box')
const quizButton = document.getElementById('quiz-button')
const quizPreInfo = document.getElementById('quiz-pre-info')
const quizContainer = document.getElementById('main-quiz-container')
const quizPostInfo = document.getElementById('quiz-post-info')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')

// Quiz Time
const timerBox = document.getElementById('timer-box')

const antivateTimer = (time) =>{
  
  if (time.toString().length < 2) {
    timerBox.innerHTML+=`<b class='ms-3 text-success'>0${time}:00</b>`
      } else {
      timerBox.innerHTML+=`<b class='ms-3'>${time}:00</b>`
      }
      
      let minutes = time-1;

  let seconds = 60
  let displaySeconds;
  let displayMinutes;

  const timer = setInterval(() => {
    seconds--
    if (seconds < 1) {
      seconds = 59
      minutes--
      
    }

    if (minutes.toString().length < 2) {
      displayMinutes = '0' + minutes 
      
      
    }else{
      displayMinutes = minutes
    }

    if (seconds.toString().length < 2) {
      displaySeconds = '0' + seconds
    } else {
      displaySeconds  = seconds
    }    


    if (minutes === 0 && seconds == 59){      
      timerBox.classList.add('text-danger')
      // alert('Your Time is up');
    }else{
      timerBox.classList.add('text-success')
    }

    if ( minutes === 0 && seconds == 1){      
      clearInterval(timer);
      sendData()
      // alert('Your Time is up');
    }
    
    
    
    timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
     

  }, 1000);
  
  
}



  
    


$.ajax(
  {
    type: 'GET',
    url: `${url}/data`,
    success: function(response){
      console.log(response)
      const data = response.data;
      data.forEach(el => {
        
        for (const [question, answers] of Object.entries(el)){
          quizBox.innerHTML += `<hr> <div class="mt-3">
                  <b>${question}</b>                
                </div> `
            answers.forEach(answer => {
              
                quizBox.innerHTML += `
                  
                <div class="">
                  <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                  <label for="${question}" > ${answer}</label>
                
                </div>

                `
              
            });

        };
        
      });
      
      
      quizContainer.classList.add('quiz-bg', 'border')
      // Remove Quiz Post Info
      quizPostInfo.classList.add('d-none')
      // Create Button
      // <button class="btn btn-sm btn-primary mt-2 border-0" type="submit" role="button" >Submit</button>
      quizButton.innerHTML += `
      <button class="btn btn-sm btn-primary mt-4 border-0" type="submit" role="button" >Submit</button>
      `
      antivateTimer(response.time)
      
    },
    error: function(error){
      console.log(error)
    },
  }


)


const quizForm = document.getElementById('quiz-form');

const csrf =  document.getElementsByName('csrfmiddlewaretoken');



const sendData  = () =>{

  const elements = [...document.getElementsByClassName('ans')];

  const data = {}
  data['csrfmiddlewaretoken'] = csrf[0].value

  elements.forEach(element => {
    if (element.checked) {
      data[element.name] = element.value
      
    } else{
      if (!data[element.name]) {
        data[element.name] = null
      }
    }
  });

  $.ajax({
    type:'POST',
    url: `${url}/save_data`,
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
    data: data,
    success: function(response) {
      const results = response.results      
      quizForm.classList.add('d-none')

      scoreBox.innerHTML +=`<p class="fw-bold p-1"> <span><i class="fa fa-asterisk text-primary" aria-hidden="true"></i></span> Pass Score: ${response.pass_score}%</p>
                    `
      resultBox.innerHTML = `${response.passed? 'Congratulations! ': 'Ups..:( '} Your Result is ${response.score.toFixed(2)}%`

      results.forEach(element => {
        const resultDiv = document.createElement('div')
        for (const [question, resp] of Object.entries(element)){

          resultDiv.innerHTML += question

          const cls = ['container', 'p-2', 'text-white', 'fs-6']
          resultDiv.classList.add(...cls)

          if (resp == 'not_answered'){
            resultDiv.innerHTML += ' - not answered'
            resultDiv.classList.add('bg-danger', 'border', 'rounded')
          } else{
            const answer = resp['answered']            
            const correct = resp['correct_answer']

            if (answer == correct){
              resultDiv.classList.add('bg-primary', 'border', 'rounded')
              resultDiv.innerHTML += ` answered: ${answer}`
            } else{
              resultDiv.classList.add('bg-danger', 'border', 'rounded')
              resultDiv.innerHTML += ` | correct answer: ${correct}`
              resultDiv.innerHTML += ` | answered: ${answer}`
            }
          }
          
        }
        
        const body = document.getElementsByTagName('BODY')[0]
        body.append(resultDiv)
        // Remove Quiz Post Info
        quizPostInfo.classList.remove('d-none')
        quizPostInfo.classList.add('d-block')
        // Remove Quiz Pre Info
        quizPreInfo.classList.add('d-none')
        // remove quiz container
        quizContainer.classList.remove('quiz-bg',)
        quizContainer.classList.add('quiz-result-bg')

        

      });
    },
    error: function(error){
      console.log(error)
    },
  })

}


quizForm.addEventListener('submit', e=>{ 
  e.preventDefault(); 
  sendData();
})
