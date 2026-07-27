import { useState } from 'react';
import { KpiCardsLeft, KpiCardsRight } from '../components/Dashboard/KpiColumns';
import { MapStage } from '../components/Maps/MapStage';
import { MapHUD } from '../components/Maps/MainHUD';

export function Dashboard() {
  const [isLocked, setIsLocked] = useState(true);
  const [isFlat, setIsFlat] = useState(false);

  return (
    <section className="relative isolate flex h-full min-w-0 flex-col gap-3 p-3">
      <MapStage isLocked={isLocked} isFlat={isFlat} />

      <div className="relative z-30 grid h-[600px] min-w-0 grid-cols-[minmax(0,15fr)_minmax(0,70fr)_minmax(0,15fr)] gap-3">
        <div className="relative z-30 min-w-0 pointer-events-auto">
          <KpiCardsLeft />
        </div>

        <div className="pointer-events-none relative min-w-0">
          <div className="pointer-events-none absolute inset-x-0 top-0 z-10 flex justify-center">
            <div className="w-full pointer-events-auto">
              <MapHUD
                isLocked={isLocked}
                setIsLocked={setIsLocked}
                isFlat={isFlat}
                setIsFlat={setIsFlat}
              />
            </div>
          </div>
        </div>

        <div className="relative z-30 min-w-0 pointer-events-auto">
          <KpiCardsRight />
        </div>
      </div>

      {/* <div className="relative z-30 grid min-w-0 flex-1 grid-cols-[minmax(0,85fr)_minmax(0,15fr)] items-stretch gap-3 pointer-events-none">
        <div className="min-w-0 pointer-events-auto">
          <RecentAlerts />
        </div>

        <div className="flex min-w-0 flex-col gap-3 pointer-events-auto">
          <div className="flex-1">
            <AlertTrend />
          </div>

          <div className="flex-1">
            <FraudByCategory />
          </div>
        </div>
      </div> */}
    </section>
  );
}
