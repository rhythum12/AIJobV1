import Navbar from './../components/Navbar.jsx';
import Footer from './../components/Footer.jsx';
export default function About() {
    return (
        <div>
            <Navbar isAuthenticated={true} />
            <div className="h-screen">
                <div className="max-w-4xl mx-auto px-4 py-10 ">
                    <h1 className="text-3xl font-bold mb-4">About Job Recommender</h1>
                    <p className="text-gray-700 text-lg mb-4">
                        Job Recommender is a smart job recommendation platform designed to connect users with the best job opportunities based on their skills, experience, and preferences.
                    </p>
                    <p className="text-gray-700 text-lg mb-4">
                        We leverage advanced resume parsing and matching algorithms to help users quickly find roles that suit them, making the job hunt faster and more personalized.
                    </p>
                    <p className="text-gray-700 text-lg">
                        Our mission is to simplify the job search experience by offering powerful tools and a user-friendly interface that empowers job seekers.
                    </p>
                </div>
            </div>
            <Footer />
        </div>
    )
}