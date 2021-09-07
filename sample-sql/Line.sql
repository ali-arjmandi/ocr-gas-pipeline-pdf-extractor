USE [pdf_db]
GO

/****** Object:  Table [dbo].[Line]    Script Date: 9/6/2019 3:29:32 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Line](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[LineNum] [nvarchar](50) NULL,
	[DocumentNo] [nvarchar](50) NULL,
	[DrawingNo] [nvarchar](50) NULL,
	[LineClass] [nvarchar](50) NULL,
	[UnitNo] [nvarchar](50) NULL,
	[PIDNo] [nvarchar](50) NULL,
	[PressDesign] [nvarchar](50) NULL,
	[TempDesign] [nvarchar](50) NULL,
	[PressOperating] [nvarchar](50) NULL,
	[TempOperating] [nvarchar](50) NULL,
	[TestFluid] [nvarchar](50) NULL,
	[PressTest] [nvarchar](50) NULL,
	[InsualtionType] [nvarchar](50) NULL,
	[InsulationThk] [nvarchar](50) NULL,
	[PaintCode] [nvarchar](50) NULL,
	[HeatTransfer] [nvarchar](50) NULL,
	[StressAnalysis] [nvarchar](50) NULL,
	[Density] [nvarchar](50) NULL,
	[SteamTracing] [nvarchar](50) NULL,
	[TracingSize] [nvarchar](50) NULL,
	[ElecTracing] [nvarchar](50) NULL,
	[NDT] [nvarchar](50) NULL,
	[PWHT] [nvarchar](50) NULL,
	[Phase] [nvarchar](50) NULL,
	[Rev] [nvarchar](50) NULL,
	[SHEETS] [nvarchar](50) NULL,
 CONSTRAINT [PK_Line] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

