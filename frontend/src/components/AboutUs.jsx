import React from "react";
import { MainLayout } from "../layouts/MainLayout";

const AboutUs = () => {
  return (
    <MainLayout>
      <section class="flex w-full h-full justify-center items-center">
        <div class="flex flex-row justify-center space-x-10 px-10 items-center">
          <div class="w-1/2">
            <h1 class="text-4xl font-bold text-center my-4">About Us</h1>
            <p class="text-justify">
              At APSS, we understand the importance of a strong online presence
              in today's digital world. That's why we're dedicated to helping
              businesses increase their online visibility and drive more traffic
              to their website through effective SEO strategies. Our team of
              experts uses the latest techniques and technologies to improve
              your search engine rankings and drive more qualified leads to your
              site. We believe that SEO is not just about getting higher
              rankings, it's about getting the right kind of traffic to your
              site, and converting that traffic into paying customers. Whether
              you're a small local business or a large enterprise, our team has
              the skills and experience to help you succeed online. We work with
              you to understand your unique business needs and goals, and tailor
              our approach to suit your specific requirements. We offer a full
              range of SEO services, including keyword research, on-page
              optimization, content creation, link building, and local SEO. Our
              team stays up-to-date with the latest industry developments and
              algorithm updates to ensure that your website is always at the
              forefront of search engine rankings. We also provide regular
              reporting and analysis to keep you informed of your progress and
              make any necessary adjustments to your strategy.{" "}
            </p>
          </div>
          <div class="w-1/2">
            <img
              src="https://optinmonster.com/wp-content/uploads/2018/04/ultimate-seo-guide.jpg"
              alt="about us"
              class="w-full h-full shadow-2xl object-cover"
            />
          </div>
        </div>
      </section>
    </MainLayout>
  );
};

export default AboutUs;
