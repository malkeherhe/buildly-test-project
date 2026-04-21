const { test, expect, request } = require('@playwright/test')

const backendUrl = process.env.PLAYWRIGHT_API_URL || 'http://127.0.0.1:8000'

async function registerUser(apiContext, email, password, role = 'learner') {
  const endpoint =
    role === 'admin'
      ? `${backendUrl}/api/account/register/admin/`
      : `${backendUrl}/api/account/register/learner/`

  const response = await apiContext.post(endpoint, {
    data: { email, password, password2: password },
  })
  expect(response.ok()).toBeTruthy()
  return response.json()
}

test('learner can log in, join a course, and start a project', async ({ page }) => {
  const apiContext = await request.newContext()
  const suffix = Date.now()
  const adminEmail = `admin.${suffix}@example.com`
  const learnerEmail = `learner.${suffix}@example.com`
  const password = 'StrongPass123!'

  const adminData = await registerUser(apiContext, adminEmail, password, 'admin')
  await registerUser(apiContext, learnerEmail, password, 'learner')

  const adminAuth = {
    Authorization: `Bearer ${adminData.tokens.access}`,
  }

  const createCourseResponse = await apiContext.post(`${backendUrl}/api/courses/create/`, {
    headers: adminAuth,
    data: {
      title: `Course ${suffix}`,
      description: 'A complete course description used for an end-to-end Playwright scenario.',
      level: 'beginner',
      category: 'web',
      estimated_duration: 12,
      is_public: true,
    },
  })
  expect(createCourseResponse.ok()).toBeTruthy()
  const courseBody = await createCourseResponse.json()
  const courseId = courseBody.course.id

  const createProjectResponse = await apiContext.post(`${backendUrl}/api/projects/create/`, {
    headers: adminAuth,
    data: {
      course_id: courseId,
      title: `Project ${suffix}`,
      description: 'A sufficiently detailed project description for end-to-end verification.',
      requirements: 'Join the course',
      objectives: 'Start a project through the UI',
      resources: 'Project brief',
      estimated_time: 5,
      level: 'beginner',
      language: 'python',
      order: 1,
    },
  })
  expect(createProjectResponse.ok()).toBeTruthy()
  const projectBody = await createProjectResponse.json()
  const projectId = projectBody.project.project_id

  await page.goto('/login')
  await page.getByTestId('login-email').fill(learnerEmail)
  await page.getByTestId('login-password').fill(password)
  await page.getByTestId('login-submit').click()

  await expect(page).toHaveURL(/dashboard/)

  await page.goto('/courses')
  await page.getByTestId(`course-details-${courseId}`).click()
  page.once('dialog', async (dialog) => {
    expect(dialog.message()).toContain('تم')
    await dialog.accept()
  })
  await page.getByTestId('join-course-button').click()
  await expect(page.getByText('أنت منضم لهذا المسار')).toBeVisible()

  await page.goto(`/projects/${projectId}`)
  page.once('dialog', async (dialog) => {
    expect(dialog.message()).toContain('تم')
    await dialog.accept()
  })
  await page.getByTestId('start-project-button').click()
  await expect(page.getByText('بدء المشروع')).toBeVisible()
})
