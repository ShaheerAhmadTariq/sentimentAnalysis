import React from "react";
import { MainLayout } from "./../layouts/MainLayout";
import { Card, CardBody } from "./../ui/Card";

const Dashboard = () => {
  return (
    <MainLayout>
      <div className="m-4 min-h-screen">
        <Card className="my-4">
          <CardBody>Dashboard</CardBody>
        </Card>
      </div>
    </MainLayout>
  );
};

export default Dashboard;
