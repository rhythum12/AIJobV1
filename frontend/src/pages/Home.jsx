import { Link } from 'react-router-dom';
import Img from './../assets/Images/Img1.jpg';
export default function Home() {

  return (
    <div className="min-h-screen bg-gray-50">
      <section className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
        <div className="container mx-auto px-4 py-16 md:py-24 flex flex-col md:flex-row items-center">
          <div className="md:w-1/2 mb-8 md:mb-0">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-4">
              Find Your Dream Job With AI Job Recommondation System
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100">
              Our AI analyzes your skills and matches you with the perfect opportunities tailored just for you.
            </p>
          </div>
          <div className="md:w-1/2 md:pl-10">
            <div className="w-full h-64 md:h-80 flex items-center justify-center">
              <img src={Img} className='rounded-3xl max-h-full' alt="img" />
            </div>
          </div>
        </div>
      </section>

      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-gray-800">How Our AI Finds Your Perfect Job</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gray-50 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-4 mx-auto">
                <span className="text-blue-600 font-bold text-xl">1</span>
              </div>
              <h3 className="text-xl font-semibold text-center mb-3 text-gray-800">Upload Your Resume</h3>
              <p className="text-gray-600 text-center">
                Our AI analyzes your skills, experience, and career preferences from your resume or manual input.
              </p>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-4 mx-auto">
                <span className="text-blue-600 font-bold text-xl">2</span>
              </div>
              <h3 className="text-xl font-semibold text-center mb-3 text-gray-800">AI Job Matching</h3>
              <p className="text-gray-600 text-center">
                Our advanced algorithm matches your profile with thousands of job listings to find your ideal opportunities.
              </p>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-4 mx-auto">
                <span className="text-blue-600 font-bold text-xl">3</span>
              </div>
              <h3 className="text-xl font-semibold text-center mb-3 text-gray-800">Apply With Confidence</h3>
              <p className="text-gray-600 text-center">
                Get personalized application tips and improve your chances with AI-powered resume optimization.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-gray-800">AI-Powered Job Search</h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div className="flex flex-col md:flex-row gap-6">

              <div>
                <h3 className="text-xl font-semibold mb-3 text-gray-800">Smart Skill Mapping</h3>
                <p className="text-gray-600">
                  Our AI identifies your key skills and competencies, mapping them to the most relevant job opportunities in your field. It even recognizes transferable skills that may qualify you for positions in adjacent industries.
                </p>
              </div>
            </div>


            <div className="flex flex-col md:flex-row gap-6">
              <div>
                <h3 className="text-xl font-semibold mb-3 text-gray-800">Personalized Recommendations</h3>
                <p className="text-gray-600">
                  Our algorithm continuously learns from your preferences and feedback, refining recommendations over time. The more you use our platform, the more tailored your job matches become.
                </p>
              </div>
            </div>

          </div>
        </div>
      </section>


      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-gray-800">Popular Job Categories</h2>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { name: 'Technology' },
              { name: 'Healthcare' },
              { name: 'Finance' },
              { name: 'Marketing'},
              { name: 'Education'},
              { name: 'Design'},
              { name: 'Sales'},
              { name: 'Engineering'},
              { name: 'Customer Service'},
              { name: 'Human Resources'},
              { name: 'Remote'},
              { name: 'Part-time'}
            ].map((category, index) => (
              <div
                key={index}
                className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 text-center cursor-default"
              >
                <h3 className="font-medium text-gray-800">{category.name}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 bg-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to Find Your Dream Job?</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Join thousands of job seekers who found their perfect match with our AI-powered job recommendations.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/registration"
              className="bg-blue-600 text-white hover:bg-blue-700 font-semibold px-8 py-3 rounded-md transition-colors duration-200"
            >
              Create Free Account
            </Link>
            <Link
              to="/loginpage"
              className="bg-blue-600 text-white hover:bg-blue-700 font-semibold px-8 py-3 rounded-md transition-colors duration-200"
            >
              Login
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};
