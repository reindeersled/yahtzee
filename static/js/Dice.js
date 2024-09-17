console.log("Dice.js connected")
class Dice{
    constructor(dice_elements, rolls_remaining_element){
        this.rolls_remaining_element= rolls_remaining_element; //integer
        this.dice_elements= dice_elements; //photo names
        this.photo_names=["blank", "one", "two", "three", "four", "five", "six"];
    }

    /**
     * Returns the number of rolls remaining for a turn
     * @return {Number} an integer representing the number of rolls remaining for a turn
    */
    get_rolls_remaining(){
        return rolls_remaining_element
    }

    /**
     * Returns an array of integers representing a current view of all five Yahtzee dice_elements
     * <br> A natural mapping is used to pair each integer with a die picture
     * <br> 0 is used to represent a "blank" die picture
     *
     * @return {Array} an array of integers representing dice values of dice pictures
    */
    get_values() {
        let photos = []
        let return_numbers = []

        for (let names in this.photo_names) {
            if (this.dice_elements == names+".svg") {
                photos.push(names);
            }
        }
        for (let num in photos) {
            if (num==1) {
                return_numbers.push(1);
            } else if (num==2) {
                return_numbers.push(2);
            } else if (num==3) {
                return_numbers.push(3);
            } else if (num==4) {
                return_numbers.push(4);
            } else if (num==5) {
                return_numbers.push(5);
            } else if (num==6) {
                return_numbers.push(6);
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
        let sum = 0
        this.dice_elements.forEach(function (name) {
            if (name == 'blank.svg') {
                sum += 0;
            } else if (name == 'one.svg') {
                sum += 1;
            } else if (name == 'two.svg') {
                sum += 2;
            } else if (name == 'three.svg') {
                sum += 3;
            } else if (name == 'four.svg') {
                sum += 4;
            } else if (name == 'five.svg') {
                sum += 5;
            } else if (name == 'six.svg') {
                sum += 6;
            }
        });
        return sum
    }

    /**
     * Calculates a count of each die face in dice_elements
     * <br> Ex - would return [0, 0, 0, 0, 2, 3] for two fives and three sixes
     *
     * @return {Array} an array of six integers representing counts of the six die faces
    */
    get_counts(){

    }

    /**
     * Performs all necessary actions to roll and update display of dice_elements
     * Also updates rolls remaining
     * <br> Uses this.set to update dice
    */
    roll(){
        let dice_values = []
        for (let i = 0; i < 5; i++){
            let dice_value = Math.floor(Math.random() * (6) + 1);
            dice_values.push(dice_value);
        }
        console.log("the rolled dice:" + dice_values)
        this.set(dice_values, this.rolls_remaining_element)
    }

    /**
     * Resets all dice_element pictures to blank, and unreserved
     * <br> Uses this.#setDice to update dice
    */
    reset(){
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
        console.log("setting dice");
        new_rolls_remaining -=1;
        for (let i=0; i<new_dice_values.length; i++) {
            if (new_dice_values[i] == 0) {
                this.dice_elements[i] = "blank.svg";
            } else if (new_dice_values[i] == 1) {
                this.dice_elements[i] = "one.svg";
            } else if (new_dice_values[i] == 2) {
                this.dice_elements[i] = "two.svg";
            } else if (new_dice_values[i] == 3) {
                this.dice_elements[i] = "three.svg";
            } else if (new_dice_values[i] == 4) {
                this.dice_elements[i] = "four.svg";
            } else if (new_dice_values[i] == 5) {
                this.dice_elements[i] = "five.svg";
            } else if (new_dice_values[i] == 6) {
                this.dice_elements[i] = "six.svg";
            } else if (new_dice_values[i] == -1) {
                this.dice_elements[i] = this.dice_elements[i];
            }
        }
    }

    

}


export default Dice;