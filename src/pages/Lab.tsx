import { Box } from "@mui/material";
import LabCard from "../components/Card";
// import SlaChart from "../components/charts/Recharts/Sla";
// import DailyVolumeChart from "../components/charts/Recharts/DailyVolume";
import TopCategoriesPieChart from "../components/charts/Recharts/TopCategoriasPie";
import NivoBarChart from "../components/charts/Nivo/NivoBar";

import { useVolumeVigente, useVolumeConsolidado } from "../hooks/useVolumePropostas"
import { useSlaDiario } from "../hooks/useSla";
import { useQueueTable } from "../hooks/useQueueTable";
import NivoLineChart from "../components/charts/Nivo/NivoLine";
import QueueTable from "../components/tables/QueueTable"

// src/pages/Home.tsx
export default function Home() {
  const { data: dataVolVigente, isLoading: isLoadingVolVigente } = useVolumeVigente();
  const { data: dataVolConsolidado, isLoading: isLoadingVolConsolidado } = useVolumeConsolidado();
  const { data: slaData, isLoading: slaLoading } = useSlaDiario();
  const { data: data, isLoading: isLoading } = useQueueTable();
  return (
    <Box sx={{
        py: 12,
        gap: 2,
    }}>
    <LabCard padding={2}>

        <NivoBarChart
            title="Ocorrências Vigente"
            subtitle={dataVolVigente?.subtitle}
            total={dataVolVigente?.total}
            media={dataVolVigente?.media}
            data={dataVolVigente?.data}
            refLineH={dataVolVigente?.refLineH}
            refLineV={dataVolVigente?.refLineV}
            refLineHLabel="Meta"
            refLineVLabel="Hoje"
            isLoading={isLoadingVolVigente}
        />

        <NivoBarChart
            title="Ocorrências Consolidada"
            subtitle={dataVolConsolidado?.subtitle}
            total={dataVolConsolidado?.total}
            media={dataVolConsolidado?.media}
            data={dataVolConsolidado?.data}
            refLineH={dataVolConsolidado?.refLineH}
            refLineV={dataVolConsolidado?.refLineV}
            refLineHLabel="Meta"
            refLineVLabel="Hoje"
            isLoading={isLoadingVolConsolidado}
        />

        <Box sx={{
            py: 2,
            display: 'grid',
            gridTemplateColumns: '2fr 2fr',
            gap: 2,
        }}>
            {/* <TopCategoriesChart /> */}
            <TopCategoriesPieChart />

            <NivoLineChart
                title="SLA"
                subtitle={slaData?.subtitle}
                data={slaData?.data}
                total={slaData?.total}
                refLineH={slaData?.meta}
                refLineHLabel="Meta"
                refLineV={slaData?.refLineV}
                refLineVLabel="Hoje"
                isLoading={slaLoading}
            />

        </Box>
        <QueueTable response={data} isLoading={isLoading} />
    </LabCard>
    
    </Box>
  )
}

// <LabCard padding={2}>
//     <DailyVolumeChart />
//     <Box sx={{
//         py: 2,
//         display: 'grid',
//         gridTemplateColumns: '2fr 2fr',
//         gap: 2,
//     }}>
//         {/* <TopCategoriesChart /> */}
//         <TopCategoriesPieChart />
//         <SlaChart />
//     </Box>
// </LabCard>