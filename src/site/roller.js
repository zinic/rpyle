window.roller = {
    onkeydown: function(e) {
        var event = e ? e : event;

        switch (event.keyCode) {
            case 10: // LF
            case 13: // CR
                roller.roll();
                break;
        }
    },

    get_seed: function() {
        var rand_seed = null;

        $.ajax({
            url: 'rand',
            async: false,

            success: function (rdata) {
                rand_seed = rdata['content']
            },

            error: function () {
                alert('Got a failure boss: ' + JSON.stringify(arguments));
            }
        });

        return rand_seed;
    },

    ASCII_0: 48,
    ASCII_9: 57,

    S_BEGIN: 1,
    S_ROLL_PREFIX: 2,
    S_DICE_SIDES: 3,
    S_DICE_MOD_VALUE: 4,

    is_whitespace: function(ch) {
        switch (ch) {
            case ' ':
            case '\t':
            case '\r':
            case 'n':
                return true;

            default:
                return false;
        }
    },

    roll: function() {
        var state = roller.S_BEGIN;
        var roll_object = {
            prefix: 1,
            sides: 1,
            modifier: null
        };

        var raw_roll_eq = $('#roll_text_input').val();
        var roll_eq = raw_roll_eq.toLowerCase();
        var part_str = '';
        var part_num = 0;

        for (var i = 0; i < roll_eq.length; i++) {
            var next_num = roll_eq.charCodeAt(i) - roller.ASCII_0;
            var next_char = roll_eq[i];

            // Skip whitespace
            if (roller.is_whitespace(next_char)) {
                continue;
            }

            switch (state) {
                case roller.S_BEGIN:
                    state = roller.S_ROLL_PREFIX;

                case roller.S_ROLL_PREFIX:
                    switch (next_char) {
                        case 'd':
                            state = roller.S_DICE_SIDES;
                            roll_object.prefix = part_num > 0 ? part_num : 1;
                            part_num = 0;
                            break;

                        default:
                            if (next_num >= 0 && next_num < 10) {
                                part_num *= 10;
                                part_num += next_num;
                            } else {
                                throw 'Bad number in number of dice. Expected format is #d#+-/*#';
                            }
                    }
                    break;

                case roller.S_DICE_SIDES:
                    switch (next_char) {
                        case '+':
                        case '-':
                        case '*':
                        case '/':
                            roll_object.sides = part_num;
                            roll_object.modifier = {
                                type: next_char,
                                value: 0
                            }

                            state = roller.S_DICE_MOD_VALUE;
                            part_num = 0;
                            break;

                        default:
                            if (next_num >= 0 && next_num < 10) {
                                part_num *= 10;
                                part_num += next_num;
                            } else {
                                throw 'Bad number in sides of dice. Expected format is #d#+-/*#';
                            }
                    }
                    break;

                case roller.S_DICE_MOD_VALUE:
                    if (next_num >= 0 && next_num < 10) {
                        part_num *= 10;
                        part_num += next_num;
                    } else {
                        throw 'Bad modifier value. Expected format is #d#+-/*#';
                    }
                    break;
            }
        }

        switch (state) {
            case roller.S_DICE_SIDES:
                roll_object.sides = part_num > 0 ? part_num : 1;
                break;

            case roller.S_DICE_MOD_VALUE:
                roll_object.modifier.value = part_num > 0 ? part_num : 1;
                break;

            default:
                throw 'Bad ending state in parser. Expected format is #d#+-/*#';
        }

        var rng_seed = roller.get_seed();
        var rng = new Math.seedrandom(rng_seed);

        var running_total = 0;
        var result_html = '<table><tbody>';

        for (var s = 0; s < roll_object.sides; s++) {
            // We add 1 since there's no 0 on a die
            var result = Math.floor(rng() * roll_object.sides) + 1;

            if (roll_object.modifier != null) {
                switch (roll_object.modifier.type) {
                    case '+':
                        result += roll_object.modifier.value;
                        break;

                    case '-':
                        result += roll_object.modifier.value;
                        break;

                    case '*':
                        result += roll_object.modifier.value;
                        break;

                    case '/':
                        result += roll_object.modifier.value;
                        break;

                    default:
                        throw 'Bad modifier symbol: ' + roll_object.modifier;
                }
            }

            running_total += result;
            result_html += '<tr><td>Roll #' + s + '</td><td>' + result + '</td></tr>';
        }

        result_html += '<tr><td>Total</td><td>' + running_total + '</td></tr>';
        result_html += '</tbody></table>';

        var result_pane = $('#result_pane');

        if (result_pane.hasClass('hidden')) {
            result_pane.removeClass('hidden')
        }

        $('#rng_seed_text').html(rng_seed);
        $('#result_text').html(result_html);
    }
}
