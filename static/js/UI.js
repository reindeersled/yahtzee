console.log("UI.js connected")
import Dice from './Dice.js';
import Gamecard from './Gamecard.js';

//-------Dice Setup--------//
let roll_button = document.getElementById('roll_button'); 
roll_button.addEventListener('click', roll_dice_handler);

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
    if (dice.get_rolls_remaining() < 1) {
        console.log("You have no more rolls!");
    } else {
        display_feedback("Rolling the dice...", "good");
        dice.roll();
    }
}

function enter_score_handler(event){
    console.log("Score entry attempted for: ", event.target.id);
    let category = event.target.id.replace("_input", "");

    if (gamecard.is_valid_score(category, Number(parseInt(event.target.value)))) {
        console.log("Score entered!")
        gamecard.update_scores();

        dice.reset();

        if (gamecard.is_finished()) {
            console.log("Congratulations! Your score was " + gamecard.get_score());
        }

    } else {
        console.log("Invalid score!")
    }
}

//------Feedback ---------//
function display_feedback(message, context){
    console.log(context, "Feedback: ", message);

}