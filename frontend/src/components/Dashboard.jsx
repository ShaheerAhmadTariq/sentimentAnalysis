import React, { useEffect, useState } from "react";
import { MainLayout } from "./../layouts/MainLayout";
import { Card, CardBody } from "./../ui/Card";
import { Table } from "flowbite-react";
import { ArrowPathIcon, PlusIcon, TrashIcon } from "@heroicons/react/24/solid";
import { Link } from "react-router-dom";

const Dashboard = () => {
  const user = JSON.parse(localStorage.getItem("userEmail"));
  const [allProjects, setallProjects] = useState([]);
  const [currentProjects, setcurrentProjects] = useState([]);
  const brandList = JSON.parse(localStorage.getItem("brandList"));
  const [currentProject, setcurrentProject] = useState(
    brandList?.length > 0
      ? brandList[0]
      : {
          p_id: -1,
        }
  );
  async function getUserProjects() {
    if (!user) return;
    try {
      const res = await fetch("http://localhost:8000/getProjects", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ u_id: user.id }),
      });
      const projects = await res.json();
      setallProjects(projects);
      setcurrentProjects(projects);
    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {
    getUserProjects();
  }, []);

  async function updateProject(projectId) {
    try {
      const res = await fetch("http://localhost:8000/updateProject", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ u_id: user.id, p_id: projectId }),
      });
      const data = await res.json();
      alert(data.message);
    } catch (error) {
      console.log(error);
    }
  }

  async function deleteProject(projectId) {
    try {
      const res = await fetch("http://localhost:8000/deleteProject", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ u_id: user.id, p_id: projectId }),
      });
      const data = await res.json();
      alert(data.message);
      const modifiedProjects = currentProjects.filter(
        (item) => item.p_id !== projectId
      );
      setcurrentProjects(modifiedProjects);
      localStorage.removeItem("brandList");
      setcurrentProject({
        p_id: -1,
      });
    } catch (error) {
      console.log(error);
    }
  }

  const changeCurrentProject = (item) => {
    setcurrentProject(item);
    localStorage.setItem(
      "brandList",
      JSON.stringify([
        {
          p_id: item.p_id,
          brandNames: [
            item.p_brand_name,
            item.p_competitor_name,
            item.p_hashtag,
          ],
        },
      ])
    );
  };
  return (
    <MainLayout currentProjectFetch={{ currentProject, projectFetch: true }}>
      <div className="m-4 min-h-screen">
        <Card className="my-4">
          <CardBody>
            <p className="text-xl font-bold">Welcome {user.username}</p>
            <p>You can manage your projects here</p>
          </CardBody>
        </Card>
        <Card className="my-4">
          <CardBody>
            <button className="p-2 rounded-md bg-green-400 my-2">
              <Link to={"/monitor"} className="flex items-center space-x-1">
                <PlusIcon className="h-5 w-5" />
                <span>Create a project</span>
              </Link>
            </button>
            <Table>
              <Table.Head>
                <Table.HeadCell>Select Project</Table.HeadCell>
                <Table.HeadCell>Project ID</Table.HeadCell>
                <Table.HeadCell>Brand Name</Table.HeadCell>
                <Table.HeadCell>Competitor Name</Table.HeadCell>
                <Table.HeadCell>Hashtag</Table.HeadCell>
                <Table.HeadCell>Created At</Table.HeadCell>
                <Table.HeadCell>Updated At</Table.HeadCell>
                <Table.HeadCell>Update</Table.HeadCell>
                <Table.HeadCell>Delete</Table.HeadCell>
              </Table.Head>
              <Table.Body>
                {currentProjects?.map((item, index) => (
                  <Table.Row key={index}>
                    <Table.Cell>
                      <input
                        onChange={() => changeCurrentProject(item)}
                        type="checkbox"
                        name=""
                        checked={currentProject.p_id === item.p_id}
                        id=""
                      />
                    </Table.Cell>
                    <Table.Cell>{item.p_id}</Table.Cell>
                    <Table.Cell>{item.p_brand_name}</Table.Cell>
                    <Table.Cell>{item.p_competitor_name}</Table.Cell>
                    <Table.Cell>{item.p_hashtag}</Table.Cell>
                    <Table.Cell>{item.p_creation_at}</Table.Cell>
                    <Table.Cell>{item.p_update_at}</Table.Cell>
                    <Table.Cell>
                      <ArrowPathIcon
                        onClick={() => updateProject(item.p_id)}
                        className="h-5 w-5 text-green-500 cursor-pointer"
                      />
                    </Table.Cell>
                    <Table.Cell>
                      <TrashIcon
                        onClick={() => deleteProject(item.p_id)}
                        className="h-5 w-5 text-red-500 cursor-pointer"
                      />
                    </Table.Cell>
                  </Table.Row>
                ))}
              </Table.Body>
            </Table>
          </CardBody>
        </Card>
      </div>
    </MainLayout>
  );
};

export default Dashboard;
