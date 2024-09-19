console.log("Dice.js connected")
class Dice{
    constructor(dice_elements, rolls_remaining_element){
        this.rolls_remaining_element= rolls_remaining_element; //html object
        this.dice_elements= dice_elements; //html element of the photo svgs
        this.photo_names=["blank", "one", "two", "three", "four", "five", "six"];
    }

    /**
     * Returns the number of rolls remaining for a turn
     * @return {Number} an integer representing the number of rolls remaining for a turn
    */
    get_rolls_remaining(){
        return Number(this.rolls_remaining_element.innerHTML);
    }

    /**
     * Returns an array of integers representing a current view of all five Yahtzee dice_elements
     * <br> A natural mapping is used to pair each integer with a die picture
     * <br> 0 is used to represent a "blank" die picture
     *
     * @return {Array} an array of integers representing dice values of dice pictures
    */
    get_values() {
        let photos = [];
        let return_numbers = [];

        for (let dice of this.dice_elements) {
            let dice_src = dice.src
            for (let names of this.photo_names) {
                if (dice_src.includes(names)) {
                    photos.push(names);
                }
            }
        }
        for (let name of photos) {
            for (let num_index=0; num_index<this.photo_names.length;num_index++) {
                if (name.includes(this.photo_names[num_index])) {
                    return_numbers.push(num_index);
                }
            }
        }
        return return_numbers
    }

    /**
     * Calculates the sum of all dice_elements
     * <br> Returns 0 if the dice are blank
     *
     * @return {Number} an integer represenitng the sum of all five dice
    */
    get_sum(){
        let sum = 0;
        for (let dice of this.dice_elements) {
            let dice_src = dice.src;
            for (let photo_index=0; photo_index<this.photo_names.length;photo_index++) {
                if (dice_src.includes(this.photo_names[photo_index])) {
                    sum += photo_index;
                }
            }
        }
        return sum;
    }

    /**
     * Calculates a count of each die face in dice_elements
     * <br> Ex - would return [0, 0, 0, 0, 2, 3] for two fives and three sixes
     *
     * @return {Array} an array of six integers representing counts of the six die faces
    */
    get_counts(){
        let count = [0,0,0,0,0,0];
        let photos = ["one", "two", "three", "four", "five", "six"];

        for (let die of this.dice_elements) {
            let die_src = die.src
            for (let photo_index=0; photo_index<photos.length;photo_index++) {
                if (die_src.includes(photos[photo_index])) {
                    count[photo_index] += 1;
                }
            }
        }
        return count
    }

    /**
     * Performs all necessary actions to roll and update display of dice_elements
     * Also updates rolls remaining
     * <br> Uses this.set to update dice
    */
    roll(){
        let dice_values = [];
        for (let i = 0; i < 5; i++){
            let dice_value = Math.floor(Math.random() * (6) + 1);
            dice_values.push(dice_value);
        }
        this.set(dice_values, Number(this.rolls_remaining_element.innerHTML-1));
    }

    /**
     * Resets all dice_element pictures to blank, and unreserved
     * <br> Uses this.#setDice to update dice
    */
    reset(){
        let new_dice_values = [0,0,0,0,0];
        this.set(new_dice_values, 3);
        for (let dice of this.dice_elements) {
            dice.classList.remove("reserved");
        }
    }

    /**
     * Performs all necessary actions to reserve/unreserve a particular die
     * <br> Adds "reserved" as a class label to indicate a die is reserved
     * <br> Removes "reserved" a class label if a die is already reserved
     * <br> Hint: use the classlist.toggle method
     *
     * @param {Object} element the <img> element representing the die to reserve
    */
    reserve(die_element){
        die_element.classList.toggle("reserved");
        console.log(die_element.getAttribute("class"))
    }

    /**
     * A useful testing method to conveniently change dice / rolls remaining
     * <br> A value of 0 indicates that the die should be blank
     * <br> A value of -1 indicates that the die is reserved and should not be updated
     *
     * @param {Array} new_dice_values an array of five integers, one for each die value
     * @param {Number} new_rolls_remaining an integer representing the new value for rolls remaining
     *
    */
    set(new_dice_values, new_rolls_remaining){
        this.rolls_remaining_element.innerHTML = new_rolls_remaining;
        for (let i=0; i<new_dice_values.length; i++) {
            if (new_dice_values[i] == 0) {
                this.dice_elements[i].src = "img/blank.svg";
            } else if (new_dice_values[i] == 1) {
                this.dice_elements[i].src = "img/one.svg";
            } else if (new_dice_values[i] == 2) {
                this.dice_elements[i].src = "img/two.svg";
            } else if (new_dice_values[i] == 3) {
                this.dice_elements[i].src = "img/three.svg";
            } else if (new_dice_values[i] == 4) {
                this.dice_elements[i].src = "img/four.svg";
            } else if (new_dice_values[i] == 5) {
                this.dice_elements[i].src = "img/five.svg";
            } else if (new_dice_values[i] == 6) {
                this.dice_elements[i].src = "img/six.svg";
            } else if (new_dice_values[i] == -1) {
                console.log("reserving...");
                this.reserve(this.dice_elements[i]);
            }
        }
    }
}


export default Dice;