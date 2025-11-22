import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/features/Layout';
import { HomePage } from './pages/HomePage';
import { AffiliatesPage } from './pages/AffiliatesPage';
import { AffiliateFormPage } from './pages/AffiliateFormPage';
import { AffiliateDetailPage } from './pages/AffiliateDetailPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30000,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path="affiliates" element={<AffiliatesPage />} />
            <Route path="affiliates/new" element={<AffiliateFormPage />} />
            <Route path="affiliates/:id" element={<AffiliateDetailPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
