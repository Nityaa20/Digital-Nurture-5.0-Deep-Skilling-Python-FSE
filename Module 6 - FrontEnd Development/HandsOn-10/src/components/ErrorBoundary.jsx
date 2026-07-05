// ErrorBoundary.jsx
// React does not let you make an error boundary using a normal function
// component with hooks, it has to be a class component, this is the only
// place in this whole project where i used a class instead of a function.

import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    // in a real project this would probably be sent to some logging service
    console.log("Something crashed:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: "20px", background: "#ffe6e6", color: "#900" }}>
          <h2>Oops, something went wrong.</h2>
          <p>Please refresh the page and try again.</p>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
