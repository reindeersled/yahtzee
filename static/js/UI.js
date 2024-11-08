console.log("UI.js connected")
import Dice from './Dice.js';
import Gamecard from './Gamecard.js';

display_feedback("Started a new game!", "good")

//-------Dice Setup--------//
let roll_button = document.getElementById('roll_button'); 
roll_button.addEventListener('click', roll_dice_handler);

let save_button = document.getElementById('save_game'); 
save_button.addEventListener('click', save_game);

let load_button = document.getElementById('load_game'); 
load_button.addEventListener('click', load_game);

let dice_elements =[];
for (let i = 0; i<5; i++){
    let die = document.getElementById("die_"+i);
    die.addEventListener('dblclick', reserve_die_handler);
    dice_elements.push(die);
}
let rolls_remainging_element = document.getElementById("rolls_remaining");
let dice = new Dice(dice_elements, rolls_remainging_element);
window.dice = dice; //useful for testing to add a reference to global window object



//-----Gamecard Setup---------//
let category_elements = Array.from(document.getElementsByClassName("category"));
for (let category of category_elements){
    category.addEventListener('keypress', function(event){
        if (event.key === 'Enter') {
            enter_score_handler(event);
        }
    });
}
let score_elements = Array.from(document.getElementsByClassName("score"));
let gamecard = new Gamecard(category_elements, score_elements, dice);
window.gamecard = gamecard; //useful for testing to add a reference to global window object


//---------Event Handlers-------//
function reserve_die_handler(event){
    dice.reserve(document.getElementById(event.target.id));
}

function roll_dice_handler(){
    console.clear();
    document.getElementById('feedback').className = '';
    document.getElementById('feedback').innerHTML = '';
    if (dice.get_rolls_remaining() < 1) {
        display_feedback("You have no more rolls!", "bad")
    } else {
        dice.roll();
    }
}

function enter_score_handler(event){
    let category = event.target.id.replace("_input", "");
    
    let dice_values = dice.get_values();
    if (dice_values.includes(0)) {
        display_feedback("You haven't rolled your dice!", "bad")
    } else {
        if (gamecard.is_valid_score(category, Number(parseInt(event.target.value)))) {
            display_feedback("Score successfully entered!", "good")
            gamecard.update_scores();
    
            dice.reset();
    
            if (gamecard.is_finished()) {
                display_feedback("Game completed!", "good")
            }
    
        } else {
            display_feedback("Invalid score!", "bad")
        }
    }
}

function load_game() {
    console.log(localStorage.getItem('yahtzee'));
    if (!localStorage.getItem('yahtzee')) {
        display_feedback("Game doesn't exist!", "bad");
    } else {
        let old_game = localStorage.getItem('yahtzee'); //string
        gamecard.load_scorecard(JSON.parse(old_game));
        display_feedback("Game loaded!", "good")
    }
}

function save_game() {
    localStorage.setItem('yahtzee', JSON.stringify(gamecard.to_object()));
    display_feedback("Game saved!", "good")
}

//------Feedback ---------//
function display_feedback(message, context){
    let feedbackElement = document.getElementById('feedback');
    feedbackElement.className = context; 
    feedbackElement.innerHTML = message;
    console.log(context, "Feedback: ", message);
}