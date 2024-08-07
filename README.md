# Adviser App

Welcome to the Adviser App! This is a comprehensive platform designed to connect sponsors with influencers for managing advertising campaigns efficiently. The app provides separate login portals for admins, sponsors, and influencers, each with specific functionalities tailored to their roles.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Usage](#usage)
- [API Resources](#api-resources)
- [Database Schema](#database-schema)
- [License](#license)

## Features

- **Admin Dashboard**: Manage users, campaigns, and monitor overall platform performance.
- **Sponsor Portal**: Create and manage advertising campaigns, assign influencers, and track campaign performance.
- **Influencer Portal**: Accept campaign assignments, upload content, and track campaign progress.
- **Data Visualization**: Interactive charts for tracking campaign performance, budgets, and more.

## Tech Stack

- **Backend**: Flask
- **Frontend**: Bootstrap, HTML, CSS
- **Database**: MySQL
- **Charts**: Chart.js

## Setup

### Prerequisites

- Python 3.8+
- MySQL
- Pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/adviser-app.git
   cd adviser-app

## Usage
### Landing Page
The landing page provides a welcome message and links to the respective login pages for Admin, Sponsor, and Influencer.

### Admin
Admins can log in and manage users, campaigns, and monitor overall performance through the admin dashboard.

###Sponsor
Sponsors can create and manage campaigns, assign influencers, and track the performance and budget of their campaigns.

### Influencer
Influencers can log in, accept campaign assignments, upload content, and track their progress and ratings.

### API Resources
- Campaign Management: APIs to create, update, and manage campaigns.
  
## Database Schema
The database includes the following main tables:
-**admins**: Stores admin user information.
-**sponsor**: Stores sponsor user information.
-**influencer**: Stores influencer user information and their ratings.
-**campaign**: Stores campaign details, including name, budget, start date, end date, etc.
-**adrequest**: Stores ad information linked to campaigns and influencers.
-**category**: Stores different categories for campaigns and influencers
-**niche**: Stores different niches which belong to some category.

