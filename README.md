# ChatVibe

ChatVibe is a full-stack web application built with Django REST Framework for the backend and React for the frontend. The application aims to provide a platform for users to engage in real-time chat conversations within categorized servers and channels, similar to popular platforms like Discord.

The backend of ChatVibe utilizes Django REST Framework to manage user authentication, server, and channel creation, as well as handling WebSocket connections for real-time communication. It also integrates with PostgreSQL database to store user data, server configurations, and chat histories.

The frontend, built with React and Material UI, offers a responsive and intuitive user interface. Users can browse through different server categories, join servers, and participate in chat rooms within each server. The frontend communicates with the backend API to fetch and send data, enabling seamless interaction and updates in real-time.

Key Features of ChatVibe include:

- User authentication and authorization using JWT tokens
- Creation and management of servers and channels
- Real-time chat functionality with WebSocket support
- Responsive design for optimal viewing on various devices
- Integration with PostgreSQL database for data storage and retrieval
- Secure communication through HTTPS and HTTP-only cookies

ChatVibe is designed to be modular, scalable, and customizable, allowing developers to extend its functionality according to their specific requirements. Whether used for team collaboration, community building, or social networking, ChatVibe provides a robust and versatile platform for real-time communication.