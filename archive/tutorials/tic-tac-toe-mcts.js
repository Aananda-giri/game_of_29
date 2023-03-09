// how to play tic-tac-toe
ticTacToeState = [0, 0, 0, 0, 0, 0, 0, 0, 0];

class TicTacNode{
    constructor(state, parent, action) {
    this.state = state;
    
    // figure out tthe move number
    this.move = state.reduce((a, v) => v > 0 ? a + 1  : a, 0);
    thhis.play = 0;

    const positions = this.validMoves(state);

    this.children = positions.map((pos) => {
        const newState = state.slice(0)
    })
    }

    validMoves(state){
        const positions = [];
        state.forEach((v, idx) => {
            if (v === 0)
                positions.push(idx);
        });
        return positions;
    }
}