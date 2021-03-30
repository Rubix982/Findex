// React
import React from 'react';

// Pages
import Home from './pages/Home';
import HomeSearch from './pages/HomeSearch';
import Accomplishments from './pages/Accomplishments';
import HowToUse from './pages/HowToUse';

// Components
import MainLayout from './components/MainLayout';

const routes = [
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { path: 'home', element: <Home /> },
      { path: 'home-search', element: <HomeSearch /> },      
      { path: 'accomplishments', element: <Accomplishments /> },      
      { path: 'how-to-use', element: <HowToUse /> },                  
    ]
  }
];

export default routes;
