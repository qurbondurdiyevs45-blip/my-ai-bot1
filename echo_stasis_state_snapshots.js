/**
 * ECHO STASIS: A lightweight, immutable state tree auditor for complex JS applications.
 * Implements a simplified Redux-like snapshotting system with diff-tracking
 * and 'Time Travel' console visualization for debugging UI reactivity.
 */

const EchoStasis = (() => {
    const history = [];
    let currentIndex = -1;
    let currentState = {};
    const listeners = new Set();

    /**
     * Deep clones an object to ensure immutability
     */
    const deepClone = (obj) => JSON.parse(JSON.stringify(obj));

    /**
     * Generates a console-friendly diff between two objects
     */
    const getDiff = (prev, next) => {
        const changes = {};
        const allKeys = new Set([...Object.keys(prev), ...Object.keys(next)]);
        allKeys.forEach(key => {
            if (JSON.stringify(prev[key]) !== JSON.stringify(next[key])) {
                changes[key] = { from: prev[key], to: next[key] };
            }
        });
        return changes;
    };

    return {
        /**
         * Initialize the state store
         * @param {Object} initialState 
         */
        init: (initialState) => {
            currentState = deepClone(initialState);
            history.push({ state: currentState, timestamp: Date.now(), delta: 'INIT' });
            currentIndex = 0;
            console.log('%c[EchoStasis] Store Initialized', 'color: #00ff88; font-weight: bold;');
        },

        /**
         * Update the state and record a snapshot
         * @param {Object} newState 
         * @param {string} actionName 
         */
        commit: (newState, actionName = 'ANONYMOUS_COMMIT') => {
            const updatedState = { ...currentState, ...deepClone(newState) };
            const delta = getDiff(currentState, updatedState);
            
            // Prune future timeline if we had traveled back
            if (currentIndex < history.length - 1) {
                history.splice(currentIndex + 1);
            }

            currentState = updatedState;
            history.push({ state: currentState, timestamp: Date.now(), delta, action: actionName });
            currentIndex++;

            listeners.forEach(fn => fn(currentState));
            
            console.groupCollapsed(`%c▶ Commit: ${actionName}`, 'color: #55aaff');
            console.log('Diff:', delta);
            console.log('Snapshot:', currentState);
            console.groupEnd();
        },

        /**
         * Travel to a specific point in time
         * @param {number} index 
         */
        travel: (index) => {
            if (index >= 0 && index < history.length) {
                currentIndex = index;
                currentState = deepClone(history[index].state);
                listeners.forEach(fn => fn(currentState));
                console.warn(`[EchoStasis] Time Travel to index ${index} (${history[index].action || 'Init'})`);
            }
        },

        subscribe: (fn) => listeners.add(fn),

        getHistory: () => history,

        getCurrent: () => currentState,

        /**
         * Export a JSON report for debugging
         */
        exportStasis: () => {
            const report = JSON.stringify(history, null, 2);
            const blob = new Blob([report], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `stasis_report_${Date.now()}.json`;
            link.click();
        }
    };
})();

// --- EXAMPLE USAGE & TEST ---

// Initialize tool
EchoStasis.init({ user: 'Guest', theme: 'dark', notifications: true });

// Subscribe a 'UI renderer' to changes
EchoStasis.subscribe((state) => {
    // In a real app, this would trigger React/Vue/D3 updates
    console.log('%cUI SYNC:', 'color: #ffaa00', state);
});

// Perform actions
setTimeout(() => {
    EchoStasis.commit({ user: 'Elite_Coder' }, 'LOGIN_SUCCESS');
}, 1000);

setTimeout(() => {
    EchoStasis.commit({ theme: 'void-obsidian', notifications: false }, 'PREFERENCE_CHANGE');
}, 2000);

setTimeout(() => {
    console.log('Rewinding to initial state...');
    EchoStasis.travel(0);
}, 4000);

// Instructions for the developer console
console.log('%c--- EchoStasis Ready ---', 'background: #222; color: #fff; padding: 5px;');
console.log('Try typing: EchoStasis.getHistory()');
console.log('Try typing: EchoStasis.commit({ data: "test" }, "CONSOLE_LOG")');